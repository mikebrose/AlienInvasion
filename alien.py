import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class to represent a single alien in the fleet"""
    def __init__(self, ai_game):
        """Initialize alien and its starting position"""
        super().__init__()
        self.screen = ai_game.screen

        #Load alien and set its rect attribute
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        #Start each alien near top left of screen
        self.rect.x = self.rect.width
        self.rect.y =  self.rect.height

        #Store the aliens exact horizontal position
        self.x = float(self.rect.x)
            

