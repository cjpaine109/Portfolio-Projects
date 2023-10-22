class GameStats:
    """Track statistics for the game"""

    def __init__(self, ai):
        """Initialize statistics"""
        self.settings = ai.settings
        self.reset_stats()


        # High score should never be reset
        self.high_score = 0

    def reset_stats(self):
        """Initialize stats that can change throughout the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1