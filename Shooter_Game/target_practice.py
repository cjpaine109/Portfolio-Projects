import sys
import pygame
from target import Target
from shooter import Shooter
from bullets import Bullet
from button import Button
from score import Score
from settings import Settings

class TargetPractice:
    """Main Class"""

    def __init__(self):
        """Initialize game and resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption('Target Practice')

        self.shooter = Shooter(self)

        self.target = Target(self)

        self.bullets = pygame.sprite.Group()

        # Make play button
        self.button = Button(self, 'Play')

        # Set game flag
        self.game_active = False

        # Init missed shots counter

        self.missed_shots = 0

        # Set up a hits counter
        self.hits = 0

        # Initialize scoreboard
        self.sb = Score(self)

    def run_game(self):
        """Main game loop"""
        while True:
            self._check_events()
            if self.game_active == True:
                self.shooter.update()
                # The line below should be removed to avoid redundancy
                # self.bullets.update()
                self._check_collisions()
                self._update_bullets()

                if self.missed_shots >= 3:
                    self.game_active = False
                    self.settings.initialize_dynamic_settings()

            self._update_screen()
            self.clock.tick(60)


    def _check_events(self):
        """Check for events"""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if not self.game_active:
                        self._check_play_button(mouse_pos)
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play"""
        button_clicked = self.button.rect.collidepoint(mouse_pos)
        if button_clicked:
            self.game_active = True
            self.missed_shots = 0 
            self.bullets.empty()
            self.hits = 0

    def _check_keydown_events(self, event):
        """Respond to keys being pressed"""
        if event.key == pygame.K_UP:
            self.shooter.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.shooter.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullets()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Respond to key being released"""
        if event.key == pygame.K_UP:
            self.shooter.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.shooter.moving_down = False

    def _fire_bullets(self):
        """Fire bullets with spacebar"""
        if len(self.bullets) <= self.settings.bullet_limit:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
        else: 
            self.game_active = False

    def _update_target(self):
        """Update target position"""
        self.target.update()
    
    def _check_collisions(self):
        """Check for collisions between bullets and the target"""
        
        # Check for bullets that have hit the target.
        # The True arguments tell Pygame to delete bullets and the target that have collided.
        collisions = pygame.sprite.spritecollide(self.target, self.bullets, True)

        if collisions:
            # For now, just print when the target is hit.
            self._target_hit()

    
    def _target_hit(self):
        """Target hit"""
        print(f"Target Hit! Current Hits: {1 + self.hits}")
        self.hits += 1
        if self.hits % 3 == 0:
            self._new_level()


    def _new_level(self):
        """Go to next level"""
        print("Congrats, you have moved to the next level!")
        self.settings.increase_speed()
        self.settings.score += 1
        self.hits = 0 # Reset hits for each level
        self.sb.prep_score()

    
    def _update_bullets(self):
        """Update bullet positions and check for bullets that have missed."""
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            if bullet.rect.left > self.screen.get_rect().right:
                print("Missed Shot!")
                self.bullets.remove(bullet)
                self.missed_shots += 1

    def _update_screen(self):
        """Update screen and draw items"""
        self.screen.fill(self.settings.bg_color)  # Clear the screen
        if self.game_active:
            self.target.update()
            self.target.draw_target()
            self.sb.show_score()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.shooter.blitme()
        if not self.game_active:
            self.button.draw_button()
            self.sb.reset_score()

        pygame.display.flip()


if __name__ == '__main__':
    target = TargetPractice()
    target.run_game()