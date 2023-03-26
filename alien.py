import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class to represent a single alien in the fleet"""
    def __init__(self, ai_game):
        """Initialize alien and its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #Load alien and set its rect attribute
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        #Start each alien near top left of screen
        self.rect.x = self.rect.width
        self.rect.y =  self.rect.height

        #Store the aliens exact horizontal position
        self.x = float(self.rect.x)
        self.speed = self.settings.alien_speed
        self.drop_speed = self.settings.alien_drop_speed

    def update(self):
        """Update position according to speed and current direction"""
        self.x += self.settings.fleet_direction * self.speed
        self.rect.x = self.x
            
    def check_edges(self):
        """Check to see if alien has reached edge of screen"""
        return (self.rect.right >= self.settings.screen_width or
            self.rect.left <= 0)


