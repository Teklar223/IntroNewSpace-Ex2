import Configuration
from pygame.locals import *
import pygame
import copy
import math
from Engine import Engine

# Constants
UP = K_w
DOWN = K_s
LEFT = K_a
RIGHT = K_d

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, config : Configuration, *groups, init_x = 0, init_y = 0 ):

        # *** Pygame ***
        super().__init__(*groups)
        self.original_image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, (255, 100, 100), [(0, 0), (25, 50), (50, 0)])
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = (init_x, init_y)
        self.paint_top_segment((100, 100, 100))

        # *** Physics ***
        self.config   =  copy.deepcopy(config) 
        self.velocity =  [config.hs, config.vs]
        self.engine   =  Engine(self.config)

        # *** Control ***
        self.is_player = False

    def paint_top_segment(self, segment_color):
        segment_width = 10  # Width of the top segment
        segment_height = 10  # Height of the top segment
    
        top_segment = pygame.Surface((segment_width, segment_height), pygame.SRCALPHA)
        pygame.draw.rect(top_segment, segment_color, (0, 0, segment_width, segment_height))
    
        self.image.blit(top_segment, (self.image.get_width() // 2 - segment_width // 2, 0))


    def up_fun(self):
        print("UP")
        self.config.NN = min(1.0, self.config.NN + 0.1)
        print("NN = ", self.config.NN)

    def down_fun(self):
        print("DOWN")
        self.config.NN = max(0.0, self.config.NN - 0.1)
    
    def left_fun(self):
        print("LEFT")
        self.config.angle = (self.config.angle + 3) % 360 # (self.config.angle + 3) % 360
        self.rotate_ship()

    def right_fun(self):
        print("RIGHT")
        self.config.angle = (self.config.angle - 3) % 360
        self.rotate_ship()
        

    def rotate_ship(self):
        self.image = pygame.transform.rotate(self.original_image, self.config.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

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
        dist,vs,hs,acc,alt,fuel,weight = engine.main_calc(dt = dt, config = self.config)
        self.config.update(dist = dist, vs = vs, hs = hs, acc = acc, alt = alt, fuel = fuel, dt = dt, weight = weight)
        self.update_position(dt = dt)
        self.ensure_bounds(width = width, height = height)

    def update_position(self, dt):
        config = self.config

        dx = 0.01 * math.sin(math.radians(config.angle)) * config.hs
        dy = 0.01 * math.cos(math.radians(config.angle)) * config.hs # Negative sign due to the inverted y-axis of pygame
        
        # Update the x and y coordinates
        self.rect.x += dx
        self.rect.y += dy

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

