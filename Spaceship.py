import Configuration
from pygame.locals import *
import pygame

# Constants
UP = K_w
DOWN = K_s
LEFT = K_a
RIGHT = K_d

class Spaceship():
    '''
    '''
    def __init__(self, config : Configuration):
        # TODO: get some of these parameters as input (the starting point) and set them via config
        self.vs     =   config.vs
        self.hs     =   config.hs
        self.dist   =   config.dist
        self.ang    =   config.ang  # zero is vertical (as in landing)
        self.alt    =   config.alt  # 2:25:40 (as in the simulation) # https://www.youtube.com/watch?v=JJ0VfRL9AMs
        self.acc    =   config.acc  # Acceleration rate (m/s^2)
        self.fuel   =   config.fuel
        self.weight =   config.WEIGHT_EMP + self.fuel
        self.NN     =   config.NN  # engine power rate (in the range [0,1]), higher = more braking power
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, config, *groups):
        # *** Pygame ***
        super().__init__(*groups)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)

        # *** Physics ***
                
        self.vs     =   config.vs
        self.hs     =   config.hs
        self.dist   =   config.dist
        self.ang    =   config.ang  # zero is vertical (as in landing)
        self.alt    =   config.alt  # 2:25:40 (as in the simulation) # https://www.youtube.com/watch?v=JJ0VfRL9AMs
        self.acc    =   config.acc  # Acceleration rate (m/s^2)
        self.fuel   =   config.fuel
        self.weight =   config.WEIGHT_EMP + self.fuel
        self.NN     =   config.NN  # engine power rate (in the range [0,1]), higher = more braking power
        self.velocity = [config.hs, config.vs]
        self.angle = config.ang

        # *** Control ***
        self.is_player = False

    def up_fun(self):
        print("UP")
        self.NN = min(1.0, self.NN + 0.1)

    def down_fun(self):
        print("DOWN")
        self.NN = max(0.0, self.NN - 0.1)
    
    def left_fun(self):
        print("LEFT")
        self.ang = (self.ang + 3) % 360

    def right_fun(self):
        print("RIGHT")
        self.ang = (self.ang - 3) % 360

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

