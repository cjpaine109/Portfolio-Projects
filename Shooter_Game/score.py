import pygame.font

class Score:
    """A class to keep track of the score"""

    def __init__(self, target):
        """Init scorekeeping attributes"""
        self.screen = target.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = target.settings

        # Font settings
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare initial score and level image
        self.prep_level()
        self.prep_score()

    def prep_score(self):
        """Turn score into rendered image"""
        score_str = str(self.settings.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)
        
        # Display the score below the "Level" text
        self.score_rect = self.score_image.get_rect()
        self.score_rect.center = self.screen_rect.center
        self.score_rect.top = self.level_image.get_rect().height + 20  # This assumes level_image has been prepared

    def prep_level(self):
        """Prepare the "Level" text"""
        self.level_image = self.font.render("Level", True, self.text_color, self.settings.bg_color)

        # Position the "Level" text at the center top of the screen
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = self.screen_rect.centerx
        self.level_rect.top = 10

    def show_score(self):
        """Draw scoreboard and level text to the screen"""
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.score_image, self.score_rect)

    def reset_score(self):
        """Reset the score/level to 0"""
        self.settings.score = 0
        self.prep_score()
