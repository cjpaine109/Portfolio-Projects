import pygame

class Shooter:
    """Class to manage the game character"""

    def __init__(self, target):
        """Initialize shooter and set its starting position"""
        self.screen = target.screen
        self.settings = target.settings
        self.screen_rect = target.screen.get_rect()

        # Load the shooter image
        self.image = pygame.image.load('Target Practice/Images/shooter.bmp')
        self.rect = self.image.get_rect()

        # Start shooter in left center of screen
        self.rect.midleft = self.screen_rect.midleft

        # Set float value for shooters exact horizontal position
        self.y = float(self.rect.y)

        # Set moving flags
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """Moving up or down"""
        if self.moving_up and self.rect.y > 0:
            self.y -= self.settings.shooter_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.shooter_speed

        # Update ships position - can't use float values
        self.rect.y = self.y

    def blitme(self):
        """Draw the shooter to the screen"""
        self.screen.blit(self.image, self.rect)