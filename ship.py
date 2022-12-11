import pygame

class Ship:
    """Class to manage the ship"""
    def __init__(self, ai_game):
        """Initialize the ship and starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship and get is rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start ship at bottom center of screen
        self.rect.midbottom = self.screen_rect.midbottom

        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        """Draw ship at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        if self.moving_right == True:
            self.rect.x += 3
        if self.moving_left == True:
            self.rect.x -= 3
