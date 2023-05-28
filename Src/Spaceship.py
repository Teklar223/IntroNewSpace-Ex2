import Src.Configuration as Configuration
from pygame.locals import *
import pygame
import copy
import math
from Src.Engine import Engine
from .Util.Util import to_pg_angle

# Constants
UP = K_w
DOWN = K_s
LEFT = K_a
RIGHT = K_d

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, config : Configuration, *groups, init_x = 0, init_y = 0 ):

        # *** Pygame ***
        super().__init__(*groups)
        self.original_image = pygame.Surface((50, 60), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, (255, 100, 100), [(self.original_image.get_width() // 2, 0), (0, self.original_image.get_height()), (self.original_image.get_width(), self.original_image.get_height())])
        pygame.draw.rect(self.original_image, (100, 100, 100), pygame.Rect(self.original_image.get_width() // 2 - 5, self.original_image.get_height() - 10, 10, 10,)) # draws a little box on the triangles ^ bottom part
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (init_x, init_y)

        # *** Physics ***
        print(config.__dict__)
        self.config   =  config
        self.velocity =  [config.hs, config.vs]

        # *** Control ***
        self.is_player = False


    def up_fun(self):
        self.config.thrust = min(1.0, self.config.thrust + 0.1)

    def down_fun(self):
        self.config.thrust = max(0.0, self.config.thrust - 0.1)
    
    def left_fun(self):
        self.config.angle = (self.config.angle + 3) % 360 # (self.config.angle + 3) % 360
        self.rotate_ship()

    def right_fun(self):
        self.config.angle = (self.config.angle - 3) % 360
        self.rotate_ship()
        

    def rotate_ship(self):
        angle = to_pg_angle(self.config.angle)
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def set_first_position(self, width: int, height: int):
        self.rect.x = int(width / 2)
        self.rect.y = int(height / 2)

    # def initiate_angle(self):
    #     self.config.angle += 120
    #     self.config.angle %= 360


    def update(self, dt, width, height, engine : Engine):
        keys = pygame.key.get_pressed()
        if keys[UP] or keys[K_UP]:
            self.up_fun()
        if keys[DOWN] or keys[K_DOWN]:
            self.down_fun()
        if keys[LEFT] or keys[K_LEFT]:
            self.left_fun()
        if keys[RIGHT] or keys[K_RIGHT]:
            self.right_fun()
        # calculate changes and update config
        lat, vs, hs, acc, alt, fuel, weight = engine.main_calc(dt = dt, config = self.config)
        self.config.update(lat = lat, vs = vs, hs = hs, acc = acc, alt = alt, fuel = fuel, dt = dt, weight = weight)
        self.update_position(dt = dt,screen_height=height)
        self.ensure_bounds(width = width, height = height)

    def update_position(self,dt, screen_height):
        config = self.config

        dx = 0.01 * math.sin(math.radians(config.angle)) * config.hs
        dy = 0.01 * math.cos(math.radians(config.angle)) * config.hs # Negative sign due to the inverted y-axis of pygame
        
        # Update the x and y coordinates
        ang = self.config.angle
        thrust = self.config.thrust
        alt = self.config.alt
        # TODO: check calculations
        if alt <= screen_height:
                if thrust >= 1.:
                    self.rect.x += dx / 4
                    self.rect.y += dy / 7
                elif thrust <= 0:
                    self.rect.x += dx
                    self.rect.y += dy
                else:
                    self.rect.x += dx * thrust
                    self.rect.y += dy * thrust

        # self.rect.x += config.hs * dt
        # self.rect.y += config.vs * dt

    def ensure_bounds(self, width, height):
        '''
            ensures ship stays within screen borders
        '''
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > height:
            self.rect.bottom = height

    def set_player(self):
         self.is_player = True
    
    def set_simulation(self):
         self.is_player = False

