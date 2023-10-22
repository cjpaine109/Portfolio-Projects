import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullets
from alien import Aliens

class AlienInvasion:
    """Overall class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        # Create instance to store game stats and create scoreboard
        self.stats = GameStats(self)
        self.stats.high_score = self.load_high_score()
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start game in active state
        self.game_active = False

        # Make the Play button
        self.play_button = Button(self, 'Play')

    def run_game(self):
        """Start the main loop for the game"""
        while True: 
            # Watch for keyboard and mouse events
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to keypresses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:
            # Move ship to the right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Move ship to the left
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            # Fire bullets
            self._fire_bullet()
        elif event.key == pygame.K_p:
            # Start the game
            self._start_game(event)
        elif event.key == pygame.K_q:
            # Exit game with 'q'
            sys.exit()
    
    def _check_keyup_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:
            # Stop moving ship to the right
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            # Stop moving ship to the left
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks 'Play' """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game settings
            self.settings.initialize_dynamic_settings()
            
            self.stats.reset_stats()
            self.sb._prep_score()
            self.sb._prep_level()
            self.sb._prep_ships()
            self.game_active = True

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse
            pygame.mouse.set_visible(False)

    def _start_game(self, event):
        """Start the game if p is pressed"""
        if event and not self.game_active:
            self.stats.reset_stats()
            self.game_active = True

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse
            pygame.mouse.set_visible(False)

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullets(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets, remove bullets once they disappear"""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to alien-bullet collisions"""

        # Check for any bullets that have hit aliens
        # If so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb._prep_score()
            self.sb.check_high_score()  

        # If all aliens have been destroyed
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb._prep_level()

    def _update_aliens(self):
        """Check if fleet is at edge, then update position"""
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien_ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens that reach the bottom
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0:
            # Decrement ships left and update scoreboard
            self.stats.ships_left -= 1
            self.sb._prep_ships()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(3.0)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have hit the bottom"""
        for aliens in self.aliens.sprites():
            if aliens.rect.bottom >= self.settings.screen_height:
                # Treat same as ship getting hit by alien
                self._ship_hit()
                break

    def _create_fleet(self):
        """Create a fleet of aliens"""
        # Create an alien and keep adding aliens unitl there is no room left
        # Spacing between aliens is one alien width and one alien height
        alien = Aliens(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            # Finished a row, reset x value, and increment y value
            current_x = alien_width
            current_y += 2 * alien_height

    def _check_fleet_edges(self):
        """Respond if any aliens have reached the edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Drop an entire fleet and change the fleets direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row"""
        new_alien = Aliens(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position  
        new_alien.rect.y = y_position 
        self.aliens.add(new_alien)

    def save_high_score(self):
        """Save the high score to a file."""
        with open('Alien Invasion/high_score.txt', 'w') as file:
            file.write(str(self.stats.high_score))

    def load_high_score(self):
        """Load the high score from a file."""
        try:
            with open('Alien Invasion/high_score.txt', 'r') as file:
                high_score = int(file.read())
        except FileNotFoundError:
            # If file does not exist, set a default high score of 0
            high_score = 0
        return high_score

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()

        # Draw aliens
        self.aliens.draw(self.screen)

        # Draw scoreboard
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()