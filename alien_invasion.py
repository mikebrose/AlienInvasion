import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall Class to manage game assets and behavior"""

    def __init__(self):
        """Initialize the game and create resources"""
        pygame.init()

        self.settings = Settings()
        self.clock = pygame.time.Clock()
        if self.settings.want_fullscreen:
            self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)    
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height

        else:
            self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()
        
            #Make most recently drawn screen visible
            pygame.display.flip()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to key presses and mouse events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

                

    def _check_keydown_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        "Respond to key releases"
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create new bullet and add to bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_bullets(self):
        """Update the positions and remove old bullets"""
        # Group() will call update() for each sprite in group
        # so self.bullets.update() ends up calling each bullet.update()
        self.bullets.update()
        for bullet in self.bullets:
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        # Check for impacts, turn of the Trues to allow object persistence
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
            False, True)
        
    def _update_aliens(self):
        """Update all the positions of the aliens"""
        self._check_fleet_edges()
        self.aliens.update()

    def _check_fleet_edges(self):
        """Check all ships to see if at an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        """Reverse the direction of the fleet, drop down"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.alien_drop_speed
        self.settings.fleet_direction *= -1


    def _create_fleet(self):
        """Create a fleet of Aliens"""
        # Make an Alien
        ref_alien = Alien(self)
        alien_width = ref_alien.rect.width 
        alien_height = ref_alien.rect.height

        current_y = alien_height
        while current_y < (self.settings.screen_height - 3.5 * alien_height):
            current_x = alien_width
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_pos, y_pos):
        """Create an alien, place it in row"""
        new_alien = Alien(self)
        new_alien.x = x_pos
        new_alien.y = y_pos
        new_alien.rect.x = x_pos
        new_alien.rect.y = y_pos

        self.aliens.add(new_alien)

    def _update_screen(self):
        """Draw a background color, ship and bullets"""

        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        
        #Make most recently drawn screen visible
        pygame.display.flip()

if __name__ ==  '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
