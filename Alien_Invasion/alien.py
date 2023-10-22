import pygame
from pygame.sprite import Sprite

class Aliens(Sprite):
    """ A class to represent a single alien in the fleet"""

    def __init__(self, ai):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai.screen
        self.settings = ai.settings

        # Load the ship image
        self.image = pygame.image.load('Alien Invasion/Images/alien.bmp')
        self.rect = self.image.get_rect()

        # Start each alien in the top left
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the aliens exact horizontal position 
        self.x = float(self.rect.x)

    def check_edges(self):
        """Check if the alien has hit the edges"""
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)
    
    def update(self):
        """Move the alien to the right or left"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x
        