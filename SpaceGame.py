import pygame
from pygame.locals import *
from random import randint
from Configuration import Configuration
from Spaceship import Spaceship

# Constants
# TODO: add arrow constants + comparisons 
UP = K_w
DOWN = K_s
LEFT = K_a
RIGHT = K_d

class SpaceGame:
    '''
    This is the 'Controller' of our simulation
    '''
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.ship = None

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False
            elif event.type == KEYDOWN:
                if event.key == UP:
                    self.ship.up_fun()
                elif event.key == DOWN:
                    self.ship.down_fun()
                elif event.key == LEFT:
                    self.ship.left_fun()
                elif event.key == RIGHT:
                    self.ship.right_fun()

        return True
    
    def start(self):
        self.startMenu()
    
    def startMenu(self):
        config = Configuration()  # kwargs = None <--> default config.
        '''
            TODO:
            1. configuration (editable)
            2. start 1-player game button (which starts game with config.is_player = True)
            3. start simulation button (we can try to simuulate bereshits landing statically, or using a method/similar)
        '''
        self.startGame(config)

    def startGame(self, config):
        self.ship = Spaceship(config)
        running = True

        while running:
            dt = self.clock.tick(60) / 1000.0
            running = self._handle_events()

            self.ship.update(dt, self.screen.get_width(), self.screen.get_height())

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.ship.image, self.ship.rect)
            pygame.display.flip()

        pygame.quit()