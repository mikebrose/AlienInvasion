import sys

import pygame

from settings import Settings

class AlienInvasion:
    """Overall Class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create resources"""
        pygame.init()

        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
        # Watch for keyboard and mouse events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            #Redraw background color
            self.screen.fill(self.settings.bg_color)

            #Make most recently drawn scree visible
            pygame.display.flip()
            self.clock.tick(60)

if __name__ ==  '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
