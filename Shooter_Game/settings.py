class Settings:
    """A class to manage the settings"""

    def __init__(self):
        """Initialize static game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 0)

        # Rectangle settings
        self.rectangle_width = 20
        self.rectangle_height = 130

        # Score settings
        self.score = 0 

        # Bullet settings
        self.bullet_width = 15
        self.bullet_height = 3
        self.bullet_color = (255, 255, 255)
        self.bullet_limit = 10

        # How quickly the game speeds up
        self.speed_up = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Init dynamic settings"""
        self.shooter_speed = 3
        self.rectangle_speed = 5
        self.bullet_speed = 6

    def increase_speed(self):
        """Increase speed settings"""
        self.shooter_speed *= self.speed_up
        self.rectangle_speed *= self.speed_up
        self.bullet_speed *= self.speed_up