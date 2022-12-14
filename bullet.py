import pygame 
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired by ship"""

    def __init__(self, ai_game):
        """Create bullet object at ship's current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # Create bullet rect at (0,0) then set to correct position
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
            self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store bullets y as float, x wont change
        self.y = float(self.rect.y)

    def update(self):
        """Update the bullet position"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet to screen"""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)