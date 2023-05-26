import math

import pygame
from pygame.locals import *
from random import randint
from Configuration import Configuration
from Spaceship import Spaceship
from Engine import Engine
from Util import InputBox,topg # to pygame (co-ordinates)
from pygame_functions import *
from game_constants import *
from Constants import *
import sys # TODO remove
# wasd Constants
UP = K_w
DOWN = K_s
LEFT = K_a
RIGHT = K_d

class SpaceGame:
    '''
    This is the 'Controller' of our simulation
    '''
    def __init__(self,width = 640, height = 480):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ship = None
        self.font = pygame.font.SysFont(None, 24)
        self.config_text_surfaces = {}
        self.config = Configuration()  # Creates a default config
        self.bg = Background()
        self.bg.setTiles(tiles=bg_name, screen=self.screen)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False

        return True
    
    def start(self):
        self.startMenu()
    
    def startMenu(self):
        input_boxes = []  # List to store the input boxes

        # Create input boxes for each configuration variable
        y_offset = 10
        for key, value in self.config.__dict__.items():
            if key not in ["WEIGHT_EMP","WEIGHT_FUEL","WEIGHT_FULL","MAIN_ENG_F","SECOND_ENG_F","MAIN_BURN","SECOND_BURN", "ALL_BURN", "is_player"]:
                permatxt = f"{key}: "
                x = self.screen.get_width() - 210
                input_box = InputBox(x, y_offset, 200, 30, text=str(value), permatext=permatxt)
                input_boxes.append(input_box)
                y_offset += 40

        start_button_rect = pygame.Rect(300, 200, 200, 100)  # Rect for the start button
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

                # Handle events for the input boxes
                for input_box in input_boxes:
                    input_box.handle_event(event, self.set_config)

            self.screen.fill((255, 255, 255))

            # Draw the start button
            pygame.draw.rect(self.screen, (0, 255, 0), start_button_rect)
            start_button_text = self.font.render("Start", True, (0, 0, 0))
            start_button_text_rect = start_button_text.get_rect(center=start_button_rect.center)
            self.screen.blit(start_button_text, start_button_text_rect)

            # Render and blit configuration values
            for input_box in input_boxes:
                input_box.update()
                input_box.draw(self.screen)

            pygame.display.flip()

            # Check if the start button is clicked
            if pygame.mouse.get_pressed()[0] and start_button_rect.collidepoint(pygame.mouse.get_pos()):
                # Update the configuration variables
                #for input_box in input_boxes:
                #    setattr(self.config, input_box.permatext, input_box.text)
                input_boxes.clear()
                self.startGame()
                running = False

    def set_config(self, key, value):
        # todo: maybe more precise validation (per paramater?)
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        if is_number(value):
            d = self.config.__dict__
            d[key[:-2]] = float(value)

    def render_config_values(self, config):
        # TODO: display up to 3 numbers after the dot (.000 but not .0000)
        y_offset = 10
        for key, value in config.__dict__.items():
            if key not in ["WEIGHT_EMP","WEIGHT_FUEL","WEIGHT_FULL","MAIN_ENG_F","SECOND_ENG_F","MAIN_BURN","SECOND_BURN", "ALL_BURN", "is_player"]:
                text = f"{key}: {value:.5f}"
                if key not in self.config_text_surfaces or self.config_text_surfaces[key] != text:
                    rendered_text = self.font.render(text, True, (255, 255, 255))
                    self.config_text_surfaces[key] = rendered_text
                text_surface = self.config_text_surfaces[key]
                text_rect = text_surface.get_rect(topright=(self.screen.get_width() - 10, y_offset))
                self.screen.blit(text_surface, text_rect)
                y_offset += 24

    def blit_config_values(self):
        for text_surface in self.config_text_surfaces.values():
            self.screen.blit(text_surface, text_surface.get_rect())

    def startGame(self):
        # Clear the screen
        # self.screen.fill((255, 255, 255))
        bg = pygame.image.load('Media/background.jpg').convert()
        scroll = 0
        tiles = math.ceil(self.screen.get_width() / bg.get_width()) + 1

        x,y = topg(self.screen.get_width()/2, 0.9 * self.screen.get_height(), self.screen.get_height())
        self.ship = Spaceship(self.config,init_x = x, init_y = y)
        self.ship.rotate_ship() # Rotate the ship to the correct angle to begin the simulation
        self.ship.set_first_position(self.screen.get_width(), self.screen.get_height())
        # self.ship.initiate_angle()
        self.engine = Engine(self.config)
        running = True
        speed_boost = 15
        bg_speed = 5
        while running:
            fuel = self.config.fuel
            alt = self.config.alt
            if alt <= 0 or fuel <= 0:
                break
            ticks = 30
            fps = self.clock.tick(ticks)
            dt = float(1 / ticks)
            # dt = 1.0
            bg_speed += speed_boost * (1 - self.config.NN) # define the background speed as a function of NN
            # self.clock.tick(10) # Determine the refresh rate
            # dt = 0.5
            running = self._handle_events()

            self.ship.update(engine=self.engine, dt=dt, width=self.screen.get_width(), height=self.screen.get_height())
            # self.screen.fill((255, 255, 255))
            ang = self.config.angle
            if ang < 5 or ang > 355: # Up
                scrollBackground(0, int(bg_speed), self.bg, self.screen)
            elif 85 < ang < 95: # Right
                scrollBackground(int(-bg_speed), 0, self.bg, self.screen)
            elif 175 < ang < 185: # Down
                scrollBackground(0, int(-bg_speed), self.bg, self.screen)
            elif 265 < ang < 275: # Left
                scrollBackground(int(bg_speed), 0, self.bg, self.screen)
            elif 95 <= ang <= 135: # (+Rigth, -Down)
                # scrollBackground(-int(bg_speed), int(bg_speed), self.bg, self.screen)
                scrollBackground(-int(bg_speed), math.floor(-0.5 * bg_speed), self.bg, self.screen)
            elif 135 < ang <= 175: # (-Right, + Down)
                # scrollBackground(math.floor(-0.5 * bg_speed), int(bg_speed), self.bg, self.screen)
                scrollBackground(-int(bg_speed), -int(bg_speed), self.bg, self.screen)
            elif 5 <= ang < 45: # (+Up, -Right)
                scrollBackground(math.floor(-0.5 * bg_speed), int(bg_speed), self.bg, self.screen)
                # scrollBackground(-int(bg_speed), -int(bg_speed), self.bg, self.screen)
            elif 45 <= ang <= 85: # (-Up, +Right)
                # scrollBackground(-int(bg_speed), math.floor(-0.5 * bg_speed), self.bg, self.screen)
                scrollBackground(-int(bg_speed), int(bg_speed), self.bg, self.screen)
            elif 275 <= ang <= 315: # (+Left, -Up)
                # scrollBackground(int(bg_speed), math.floor(-0.5 * bg_speed), self.bg, self.screen)
                scrollBackground(int(bg_speed), int(bg_speed), self.bg, self.screen)
            elif 315 < ang <= 355: # (-Left, +Up)
                # scrollBackground(int(bg_speed), -int(bg_speed), self.bg, self.screen)
                scrollBackground(math.floor(0.5 * bg_speed), int(bg_speed), self.bg, self.screen)
            elif 185 <= ang <= 225: # (+Down, -Left)
                # scrollBackground(math.floor(0.5 * bg_speed), int(bg_speed), self.bg, self.screen)
                scrollBackground(int(bg_speed), -int(bg_speed), self.bg, self.screen)
            else: # (-Down, +Left)
                # scrollBackground(int(bg_speed), int(bg_speed), self.bg, self.screen)
                scrollBackground(int(bg_speed), math.floor(-0.5 * bg_speed), self.bg, self.screen)
            # Render and blit configuration values
            self.render_config_values(self.ship.config)
            self.screen.blit(self.ship.image, self.ship.rect)

            pygame.display.flip()
            bg_speed = 5
        while True:
            continue

        pygame.quit()