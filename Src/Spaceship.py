import Src.Configuration as Configuration
# import Configuration as Configuration
from pygame.locals import *
import pygame
import copy
import math
from Src.Engine import Engine
# from Engine import Engine
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
        self.config   =  config
        # self.velocity =  [config.hs, config.vs]
        self.time_factor = 1 # determines the factor by which we multiply the dt (see speed_fun)

        # *** Control ***
        self.is_player = False


    def up_fun(self):
        self.config.thrust = min(1.0, self.config.thrust + 0.1)

    def down_fun(self):
        self.config.thrust = max(0.0, self.config.thrust - 0.1)
    
    def left_fun(self):
        self.config.angle = (self.config.angle + 3) % 360 # (self.config.angle + 3) % 360

    def right_fun(self):
        self.config.angle = (self.config.angle - 3) % 360
        

    def rotate_ship(self):
        angle = to_pg_angle(self.config.angle)
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def set_first_position(self, width: int, height: int):
        self.rect.x = int(width / 2)
        self.rect.y = int(height / 2)

    def speed_func(self):
        '''
            if self.time_factor == 1:
                self.time_factor +=1
            else:
                self.time_factor -=1
        '''
        if self.time_factor == 1:
            self.time_factor = 10
        else:
            self.time_factor = 1

    def check_landing(self, alt):
        if alt <= 0:
            alt = 0
        return alt

    def update(self, dt, width, height, engine : Engine, player_input = True):
        keys = pygame.key.get_pressed()
        if keys[UP] or keys[K_UP]:
            if player_input:
                self.up_fun()
        if keys[DOWN] or keys[K_DOWN]:
            if player_input:
                self.down_fun()
        if keys[LEFT] or keys[K_LEFT]:
            if player_input:
                self.left_fun()
        if keys[RIGHT] or keys[K_RIGHT]:
            if player_input:
                self.right_fun()
        if keys[K_x]:
            if player_input:
                self.speed_func()
        # calculate changes and update config
        self.rotate_ship()
        dt = dt * self.time_factor
        current_lat = self.config.lat
        lat, vs, hs, acc, alt, fuel, weight = engine.main_calc(dt = dt, config = self.config)
        alt = self.check_landing(alt = alt) # ensures alt >= 0
        self.config.update(lat = lat, vs = vs, hs = hs, acc = acc, alt = alt, fuel = fuel, dt = dt, weight = weight)
        #self.update_position(screen_height = height, ground_height = g_height,threshold=threshold, dlat = current_lat - lat)
        self.ensure_bounds(width = width, height = height)

    def update_position(self,screen_height,ground_height, threshold, dlat):
        alt = self.config.alt
        if alt < threshold:
            self.rect.x -= dlat
            self.rect.y = screen_height - ground_height - alt # pygame shenanigans

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

