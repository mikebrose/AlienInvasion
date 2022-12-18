class Settings:
    def __init__(self):
        """Initialize the game settings"""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.want_fullscreen = True
        
        # Ship Settings
        self.ship_speed = 5

        # Bullet Settings
        self.bullet_speed = 10.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 201, 20) 
        self.bullets_allowed = 30
        
        