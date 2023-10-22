import pygame
from settings import Settings

class Target:
    """Create moving rectangle"""

    def __init__(self, target):
        """Create rect and set its position"""
        self.screen = target.screen
        self.settings = target.settings

        # Create rectangle
        self.rect = pygame.Rect(0, 0, self.settings.rectangle_width, self.settings.rectangle_height)

        # Place rectangle
        self.rect.right = self.screen.get_rect().right

        # Center rectangle
        self.rect.centery = self.screen.get_rect().centery

        # Store rectangles exact verticle position
        self.y = float(self.rect.y)

        # Set game flag
        self.moving_up = True


    def update(self):
        """Move target upwards"""
        # Determine moving up/moving down
        if self.moving_up:
            self.y -= self.settings.rectangle_speed
        else:
            self.y += self.settings.rectangle_speed

        # Check if rectangle has reached the top of the screen
        if self.rect.top <= 0:
            self.moving_up = False
        # Check if rectangle has reached the bottom of the screen
        elif self.rect.bottom >= self.screen.get_rect().bottom:
            self.moving_up = True

        # Rectangle position matches calculated position for self.y
        self.rect.y = self.y
    
    def draw_target(self):
        """Draw the rectangle to the screen"""
        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)  # Using white color for the rectangle

