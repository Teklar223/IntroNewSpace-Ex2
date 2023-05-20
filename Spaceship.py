import Configuration
from pygame.locals import *
import pygame
import copy

# Constants
UP = K_w
DOWN = K_s
LEFT = K_a
RIGHT = K_d

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, config : Configuration, *groups):
        # *** Pygame ***
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)

        # *** Physics ***
        self.config   =  copy.deepcopy(config) 
        self.velocity =  [config.hs, config.vs]

        # *** Control ***
        self.is_player = False

    def up_fun(self):
        print("UP")
        self.config.NN = min(1.0, self.config.NN + 0.1)

    def down_fun(self):
        print("DOWN")
        self.config.NN = max(0.0, self.config.NN - 0.1)
    
    def left_fun(self):
        print("LEFT")
        self.config.angle = (self.config.angle + 3) % 360

    def right_fun(self):
        print("RIGHT")
        self.config.angle = (self.config.angle - 3) % 360

    def update(self, dt, width, height):

        keys = pygame.key.get_pressed()
        if keys[UP]:
            self.rect.y -= 1 # self.config.vs * dt
        if keys[DOWN]:
            self.rect.y += 1 # self.config.vs * dt
        if keys[LEFT]:
            self.rect.x -= 1 # self.config.hs * dt
        if keys[RIGHT]:
            self.rect.x += 1 # self.config.hs * dt

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

