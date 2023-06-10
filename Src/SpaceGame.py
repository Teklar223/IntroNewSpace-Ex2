import csv
import os
import random
from copy import deepcopy
from Src.Util.SavePopUp import show_popup, run_popup
from Src.Util.FileHandler import load, save
from Src.GuidingArrow import get_angle, distance
from Src.Util.Dashboard import create_dashboard
import pygame
from pygame.locals import *
from random import randint
from Src.Configuration import Configuration
from Src.Spaceship import Spaceship
from Src.Engine import Engine
from Src.Util.Util import FONT, InputBox, to_pg_coords, to_pg_angle  # to pygame (co-ordinates)
from Src.Util.pygame_functions import *
from Src.game_constants import *
from Src.Constants import *
from Src.SpaceLogger import Logger
from Src.Util.BackButton import BackButton
from Src.Util.FileHandler import save, load
# wasd Constants
UP = K_w
DOWN = K_s
LEFT = K_a
RIGHT = K_d

def attribute_names(attribute: str):
    if attribute == "vs":
        return "Vertical speed"
    elif attribute == "hs":
        return "Horizontal speed"
    elif attribute == "alt":
        return "Altitude"
    elif attribute == "lat":
        return "Latitude"
    elif attribute == "acc":
        return "Acceleration"
    elif attribute == "angle":
        return "Angle"
    elif attribute == "fuel":
        return "Fuel"
    elif attribute == "weight":
        return "Weight"
    elif attribute == "thrust":
        return "Thrust"
    elif attribute == "time":
        return "Time"
    else:
        print(attribute)
        return None



def _config_zero():
    kwargs = {
        f"{c_vertical_speed}": 0.0,
        f"{c_horizontal_speed}": 0.0,
        f"{c_angle}": 90.0,
        f"{c_engine_power}": 0.0,
        f"{c_latitude}": 0.0,
        f"{c_altitude}": 1000
    }
    return kwargs


class SpaceGame:
    '''
    This is the 'Controller' of our simulation
    '''

    def __init__(self, width=800, height=600, fullscreen_flag = None):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height),fullscreen_flag)
        self.clock = pygame.time.Clock()
        self.ship = None
        self.font = pygame.font.SysFont(None, 24)
        self.config_text_surfaces = {}
        self.config = Configuration(**_config_zero())  # Creates a default config
        self.target = (0, 0)
        self.bg = Background()
        self.ground_color = (128, 128, 128)  # Define the color of the ground floor
        self.logger = Logger()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return False

        return True

    def clear_screen(self, R=255, G=255, B=255):
        self.screen.fill((R, G, B))  # Fill the screen with black color

    def start(self):
        os.chdir("..")  # CWD is Src/Util when runtime raches this point (for some reason)
        self.startMenu()

    def startMenu(self):
        self.clear_screen()
        self.config = Configuration(**_config_zero())
        bg = pygame.image.load('Media/background.jpg').convert()
        scaled_bg = pygame.transform.scale(bg, (self.screen.get_width(), self.screen.get_height()))
        input_boxes = []  # List to store the input boxes

        # Create input boxes for each configuration variable
        y_offset = 10
        for key, value in self.config.__dict__.items():
            if key not in ["WEIGHT_EMP", "WEIGHT_FUEL", "WEIGHT_FULL", "MAIN_ENG_F", "SECOND_ENG_F", "MAIN_BURN",
                           "SECOND_BURN", "ALL_BURN", "is_player"]:
                permatxt = f"{key}: "
                x = self.screen.get_width() - 210
                input_box = InputBox(x, y_offset, 200, 30, text=str(value), permatext=permatxt)
                input_boxes.append(input_box)
                y_offset += 40
        title_font = pygame.font.Font(None, 56)
        title_surface = title_font.render("Space Simulation", True, (255, 255, 255))
        title_pos = (self.screen.get_width()/2,100)
        title_rect = title_surface.get_rect(center=title_pos)

        start_button_rect = pygame.Rect(self.screen.get_width()/2, 250, 200, 100)  # Rect for the start button
        start_button_rect.center = (self.screen.get_width()/2,200)
        simulation_button_rect = pygame.Rect(self.screen.get_width()/2, 400, 200, 100)  # Rect for the start button
        simulation_button_rect.center = (self.screen.get_width()/2,350)
        explanation_button_rect = pygame.Rect(self.screen.get_width()/2, 400, 200, 100)  # Rect for the start button
        explanation_button_rect.center = (self.screen.get_width()/2,500)
        
        save_config_rect = pygame.Rect(self.screen.get_width() - 200,y_offset,75,50)
        load_config_rect = pygame.Rect(self.screen.get_width() - 100,y_offset,75,50)
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
            self.screen.blit(scaled_bg, (0,0))
            self.screen.blit(title_surface, title_rect)

            # Draw the start button
            self.draw_single_player(start_button_rect)
            self.draw_simulation(simulation_button_rect)
            self.draw_explanation(explanation_button_rect)
            self.draw_save_and_load(save_rect= save_config_rect, load_rect= load_config_rect)

            # Render and blit configuration values
            for input_box in input_boxes:
                input_box.update()
                input_box.draw(self.screen)

            pygame.display.flip()

            # Check if the start button is clicked
            if pygame.mouse.get_pressed()[0]:

                if start_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.config.is_player = True
                    input_boxes.clear()
                    self.startGame()
                    running = False
                    continue

                if simulation_button_rect.collidepoint(pygame.mouse.get_pos()):
                    self.config.is_player = False
                    input_boxes.clear()
                    self.StartSim()
                    running = False

                if save_config_rect.collidepoint(pygame.mouse.get_pos()):
                    path = save()
                    self.logger.log_csv([self.config],path = path, active = True)
                
                if load_config_rect.collidepoint(pygame.mouse.get_pos()):
                    path = load()
                    dict = self.load_csv_file(file_object=path)[0]
                    self.config.update(dict)

    def StartSim(self):
        self.clear_screen()
        selected_file = self.select_file()
        config_list = self.load_csv_file(file_object = selected_file)
        if config_list:
            img_path = os.path.join(os.getcwd(), "Media")
            img_path = os.path.join(img_path, "back_button.png")
            img = pygame.image.load(img_path)
            back_button = BackButton((10, 10), img)
            bg = pygame.image.load('Media/background.jpg').convert()
            arrow = pygame.image.load('Media/arrow.png')

            arrow = pygame.transform.scale(arrow, (60, 100))
            grid_size = 20
            grid = []
            for i in range(grid_size):
                row = [bg_name for i in range(grid_size)]
                grid.append(row)
            event_i = random.randint(0, grid_size - 1)
            event_j = random.randint(0, grid_size - 1)
            grid[event_i][event_j] = death_star
            # self.bg.setTiles(tiles=[bg_name, 'Media/death_star.jpeg', 'Media/knowhere.jpg'], screen=self.screen)
            self.bg.setTiles(tiles=grid, screen=self.screen)
            x, y = to_pg_coords(self.screen.get_width() / 2, 0.9 * self.screen.get_height(), self.screen.get_height())
            self.ship = Spaceship(self.config, init_x=x, init_y=y)
            self.ship.rotate_ship()  # Rotate the ship to the correct angle to begin the simulation
            self.ship.set_first_position(self.screen.get_width(), self.screen.get_height())
            self.engine = Engine(self.config)

            running = True
            i = 0

            while running:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        return

                    # Handle keyboard events
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            running = False
                        elif event.key == K_BACKSPACE:
                            running = False
                            self.startMenu()  # return to main menu

                    # Handle mouse events
                    if event.type == MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        if back_button.is_clicked(mouse_pos):
                            running = False
                            self.startMenu()  # return to main menu

                dt = 1 / self.clock.tick(60)
                self.ship.config.update(**config_list[i])
                i += 1
                self.ship.update(engine=self.engine,
                                 dt=dt,
                                 width=self.screen.get_width(),
                                 height=self.screen.get_height(),
                                 player_input=False
                                 )
                running = self.end_condition()

                self.render_background()
                self.render_arrow(arrow=arrow)
                self.render_config(self.ship.config)
                self.render_ground(screen=self.screen)
                self.screen.blit(self.ship.image, self.ship.rect)
                back_button.draw(self.screen)

                pygame.display.flip()

            self.EndGame(is_sim=True)
        else:
            return  # file not valid

    def load_csv_file(self, file_object):
        arr_of_dict = [{k: float(v) for k, v in row.items()} for row in csv.DictReader(file_object, skipinitialspace=True)]
        return arr_of_dict
    
    def load_json_file(self, file_object):
        # TODO
        dict = {}
        return dict
    
    def select_file(self):
        file_path = load()
        return file_path

    def draw_save_and_load(self, save_rect, load_rect):
        color = (182,23,235)
        pygame.draw.rect(self.screen, color, save_rect)
        button_text = self.font.render("Save", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=save_rect.center)
        self.screen.blit(button_text, button_text_rect)
        pygame.draw.rect(self.screen, color, load_rect)
        button_text = self.font.render("Load", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=load_rect.center)
        self.screen.blit(button_text, button_text_rect)

    def draw_single_player(self, rect):
        pygame.draw.rect(self.screen, (0, 255, 0), rect)
        button_text = self.font.render("Single Player", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, button_text_rect)

    def draw_simulation(self, rect):
        pygame.draw.rect(self.screen, (0, 255, 0), rect)
        button_text = self.font.render("Replay", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, button_text_rect)

    def draw_explanation(self, rect):
        pygame.draw.rect(self.screen, (0, 255, 0), rect)
        button_text = self.font.render("Explanation", True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, button_text_rect)

    def set_config(self, key, value):
        # TODO: maybe more precise validation (per paramater?)
        def is_number(s):
            try:
                float(s)
                return True
            except ValueError:
                return False

        if is_number(value):
            d = self.config.__dict__
            d[key[:-2]] = float(value)

    def render_config(self, config):
        # TODO: display up to 3 numbers after the dot (.000 but not .0000)
        # TODO: display avg of the previous x dt for every param? (say avg speed in the last 5 dt)
        y_offset = 10
        # create_dashboard(self.screen, self.screen.get_width(), self.screen.get_height())
        for key, value in config.__dict__.items():
            if key not in ["WEIGHT_EMP", "WEIGHT_FUEL", "WEIGHT_FULL", "MAIN_ENG_F", "SECOND_ENG_F", "MAIN_BURN",
                           "SECOND_BURN", "ALL_BURN", "is_player"]:
                text = f"{attribute_names(key)}: {value:.5f}"
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

    def render_background(self):
        # if self.ship.config.alt > self.ground_threshold:
        # get the opposite speeds (cause we want the image to go in the other direction the ships is 'going')
        hs = -self.config.hs
        vs = -self.config.vs
        scrollBackground(int(hs), -int(vs), self.bg, self.screen)  # y is negative due to pygame
        # double negative is left for understanding :)

        # create_dashboard(self.screen, self.screen.get_width(), self.screen.get_height())

    def render_arrow(self, arrow):
        moon_coordinates = [0, 0]  # static target for easy calculations...
        x_arrow = 60
        y_arrow = 60
        x_space = int(self.config.lat)
        y_space = int(self.config.alt)
        space_coordinates = [x_space, y_space]
        arrow_angle = to_pg_angle(get_angle(space_coordinates, moon_coordinates))
        rotated_arrow = pygame.transform.rotate(arrow, arrow_angle)
        rotated_rectangle = rotated_arrow.get_rect(center=(x_arrow, y_arrow))
        self.screen.blit(rotated_arrow, rotated_rectangle)

    def render_time_factor(self, screen):
        time_factor_text = FONT.render(f"X{self.ship.time_factor}", True, (255, 255, 255))
        screen.blit(time_factor_text, (10, 10))  # Adjust the position as needed

    def render_ground(self, screen):
        # Check if the ship is below the ground height threshold
        alt = self.ship.config.alt
        screen_height = self.screen.get_height()
        ship_height = self.ship.original_image.get_height()
        threshold = 0.5 * screen_height - ship_height
        if alt <= threshold:
            # Render the ground floor
            ground_height = screen_height - self.calc_ground(alt=alt, max_val=threshold)
            # left, top = to_pg_coords(x = 0, y = ground_height, canvas_height = screen_height)
            # width, height = to_pg_coords(x = screen.get_width(), y = ground_height, canvas_height = screen_height)
            ground_rect = pygame.Rect(0, ground_height, screen.get_width(), screen_height)
            pygame.draw.rect(screen, self.ground_color, ground_rect)

    def calc_ground(self, alt, max_val):
        x1 = 0
        y1 = max_val
        x2 = max_val
        y2 = 0
        m = (y2 - y1) / (x2 - x1)
        ground_height = m * alt + max_val
        return ground_height

    def end_condition(self) -> bool:
        alt = self.ship.config.alt
        if alt > 0:
            return True
        else:
            return False

    def check_victory(self) -> bool:
        vs = self.ship.config.vs
        hs = self.ship.config.hs
        angle = self.ship.config.angle
        if -5 <= vs and -5 < hs < 5 and 85 < angle < 95:
            return True
        else:
            return False

    def startGame(self):
        self.clear_screen()
        bg = pygame.image.load('Media/background.jpg').convert()
        arrow = pygame.image.load('Media/arrow.png')
        config_list = [deepcopy(self.config)]
        arrow = pygame.transform.scale(arrow, (60, 100))
        grid_size = 20
        grid = []
        for i in range(grid_size):
            row = [bg_name for i in range(grid_size)]
            grid.append(row)
        event_i = random.randint(0, grid_size - 1)
        event_j = random.randint(0, grid_size - 1)
        grid[event_i][event_j] = death_star
        # self.bg.setTiles(tiles=[bg_name, 'Media/death_star.jpeg', 'Media/knowhere.jpg'], screen=self.screen)
        self.bg.setTiles(tiles=grid, screen=self.screen)
        x, y = to_pg_coords(self.screen.get_width() / 2, 0.9 * self.screen.get_height(), self.screen.get_height())
        self.ship = Spaceship(self.config, init_x=x, init_y=y)
        self.ship.rotate_ship()  # Rotate the ship to the correct angle to begin the simulation
        self.ship.set_first_position(self.screen.get_width(), self.screen.get_height())
        self.engine = Engine(self.config)
        self.logger.log_csv([self.ship.config], active=self.config.is_player)  # once to log the starting condition
        # active is set this way becuase were reading from an existing CSV if were simulating
        running = True
        create_dashboard(self.screen, self.screen.get_width(), self.screen.get_height())
        while running:
            dt = 1 / self.clock.tick(60)
            running = self._handle_events()

            self.ship.update(engine=self.engine,
                             dt=dt,
                             width=self.screen.get_width(),
                             height=self.screen.get_height()
                             )
            # self.logger.log_csv(self.ship.config, active = self.config.is_player) # log after every update
            running = self.end_condition()

            self.render_background()
            self.screen.blit(self.ship.image, self.ship.rect)
            self.render_arrow(arrow=arrow)
            self.render_config(self.ship.config)
            self.render_time_factor(screen=self.screen)
            self.render_ground(screen=self.screen)
            config_list.append(deepcopy(self.config))

            pygame.display.flip()

        # run_popup(self.config)
        pygame.display.update()
        self.EndGame(config_list=config_list)

    def EndGame(self, config_list: list = None, is_sim = False):
        # TODO...
        flag = self.check_victory()
        running = True

        out = show_popup(config_list, show_save=not is_sim)
        if out:
            self.startMenu()
        else:
            pygame.quit()
