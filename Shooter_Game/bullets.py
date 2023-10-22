import pygame 
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the character"""

    def __init__(self, target):
        """Create a bullet object at the characters current position"""
        super().__init__()
        self.screen = target.screen
        self.settings = target.settings
        self.color = self.settings.bullet_color

        # Create a bullet and place it at (0,0) and then set the correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.right = target.shooter.rect.right
        self.rect.centery = target.shooter.rect.centery

        # Store the bullets position as a float
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet up the screen"""
        # Update exact position of the bullet
        self.x += self.settings.bullet_speed
        # Update rect position 
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
        