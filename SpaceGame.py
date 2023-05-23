import pygame
from pygame.locals import *
from random import randint
from Configuration import Configuration
from Spaceship import Spaceship
from Engine import Engine
from Util import topg # to pygame (co-ordinates)
from Constants import *

# wasd Constants
UP = K_w
DOWN = K_s
LEFT = K_a
RIGHT = K_d

class SpaceGame:
    '''
    This is the 'Controller' of our simulation
    '''
    def __init__(self,width = 1600, height = 800):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ship = None
        self.font = pygame.font.SysFont(None, 24)
        self.config_text_surfaces = {}

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False

        return True
    
    def start(self):
        self.startMenu()
    
    def startMenu(self):
        '''
            TODO:
            1. configuration (editable)
            2. start 1-player game button (which starts game with config.is_player = True)
            3. start simulation button (we can try to simuulate bereshits landing statically, or using a method/similar)
        '''
        config = Configuration()  # kwargs = None <--> default config.
        start_button_rect = pygame.Rect(300, 200, 200, 100)  # Rect for the start button
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if start_button_rect.collidepoint(event.pos):
                        self.startGame(config)

            # Clear the screen
            self.screen.fill((255, 255, 255))

            # Draw the start button
            pygame.draw.rect(self.screen, (0, 255, 0), start_button_rect)
            start_button_text = self.font.render("Start", True, (0, 0, 0))
            start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)
            self.screen.blit(start_button_text, start_button_text_rect)

            # Render and blit configuration values
            self.render_config_values(config)

            pygame.display.flip()

    def render_config_values(self, config):
        # TODO: render only the values we care about
        y_offset = 10
        for key, value in config.__dict__.items():
            text = f"{key}: {value}"
            if key not in self.config_text_surfaces or self.config_text_surfaces[key] != text:
                rendered_text = self.font.render(text, True, (0, 0, 0))
                self.config_text_surfaces[key] = rendered_text
            text_surface = self.config_text_surfaces[key]
            text_rect = text_surface.get_rect(topright=(self.screen.get_width() - 10, y_offset))
            self.screen.blit(text_surface, text_rect)
            y_offset += 24

    def blit_config_values(self):
        for text_surface in self.config_text_surfaces.values():
            self.screen.blit(text_surface, text_surface.get_rect())

    def startGame(self, config):
        x,y = topg(self.screen.get_width()/2, 0.9 * self.screen.get_height(), self.screen.get_height())
        self.ship = Spaceship(config,init_x = x, init_y = y)
        self.engine = Engine(config)
        running = True

        while running:
            dt = self.clock.tick(60) / 100.0
            running = self._handle_events()

            self.ship.update(engine=self.engine, dt=dt, width=self.screen.get_width(), height=self.screen.get_height())

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.ship.image, self.ship.rect)

            # Render and blit configuration values
            self.render_config_values(self.ship.config)

            pygame.display.flip()

        pygame.quit()