import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button

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
        #Create instance of the Game to store stats
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        self.game_active = False
        self.play_button = Button(self, "Play")

    # def init_dynamic_settings(self):
    #     """These settings will be changed as game progresses, 
    #        but will need to be reset """
    #     self.ship.speed = self.settings.ship_speed
    #     self.bullet_speed = 2.5
    #     self.alien_speed = 1.0
    #     self.   alien_drop_speed = 1.0 

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            if self.game_active:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
   
    def _check_play_button(self, mouse_pos):
        """Start new game if play clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if (button_clicked and self.game_active == False):    
            self.game_active = True
            self.stats.reset_stats()
            self.bullets.empty()
            self.aliens.empty()

            self._create_fleet()
            self.ship.center_ship()
            # This sets some of the speeds back to default
            self.settings.reset_dynamic()
            pygame.mouse.set_visible(False)

            
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

    def _check_bullet_alien_collisions(self):
    # Check for impacts, turn on the Trues to allow object persistence
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens,
                                                True, True)  
        
    def _update_bullets(self):
        """Update the positions and remove old bullets"""
        # Group() will call update() for each sprite in group
        # so self.bullets.update() ends up calling each bullet.update()
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()
        
        if not self.aliens: 
            self.bullets.empty()
            self._create_fleet()
            # Increase the speed whenever fleet is destroyed
            self.increase_speed()


    def _update_aliens(self):
        """Update all the positions of the aliens"""
        self._check_fleet_edges()
        self.aliens.update()


        #look for ship collison
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #check for aliens reaching bottom of screen
        self._check_aliens_bottom()


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

    def increase_speed(self):
        self.settings.alien_speed *= self.settings.speedup_factor
        self.settings.alien_drop_speed *= self.settings.speedup_factor
        self.settings.bullet_speed *= self.settings.speedup_factor 
        self.settings.ship_speed *= self.settings.speedup_factor * .9

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

    def _check_aliens_bottom(self):
        """Check for any alien ships reaching bottom of screen, respond if so"""

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # act as if ship was hit
                self._ship_hit()
                break


    def _ship_hit(self):
        """Respond to ship being hit by alien"""
        if self.stats.ships_left > 0:
            #Decrement ship count
            self.stats.ships_left -= 1
            print("Ships left: ", self.stats.ships_left)
            #Get rid of remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            #create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            print("Ship Speed: ",self.settings.ship_speed)
            print("Bullet Speed: ",self.settings.bullet_speed)
            print("Alien Speed: ",self.settings.alien_speed)
            print("Alien Drop Speed: ",self.settings.alien_drop_speed)
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Draw a background color, ship and bullets"""

        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        
        if self.game_active == False:
            self.play_button.draw_button()
        
        #Make most recently drawn screen visible
        pygame.display.flip()

if __name__ ==  '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()
