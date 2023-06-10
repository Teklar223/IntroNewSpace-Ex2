import sys
# from Src.Util.FileHandler import save
from Src.Util.FileHandler import save
import pygame
from pygame.locals import *
from Src.SpaceLogger import Logger
# Step 1: Initialize Pygame
pygame.init()

# Step 2: Set up the display window
screen = pygame.display.set_mode((1000, 200))
pygame.display.set_caption("Popup Example")

# Step 3: Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

yes_button = None
no_button = None
# Step 5: Create the popup function
def show_popup(config_list: list,msg, show_save = True) -> bool:
    global no_button
    global yes_button
    popup_width = 450
    popup_height = 150
    popup_x = int((screen.get_width() - popup_width) // 2)
    popup_y = int((screen.get_height() - popup_height) - 50)

    popup_surface = pygame.Surface((popup_width, popup_height))
    popup_surface.fill(WHITE)
    pygame.draw.rect(popup_surface, BLACK, (0, 0, popup_width, popup_height), 3)
    font = pygame.font.Font(None, 24)

    text = font.render(msg, True, BLACK)
    text_rect = text.get_rect(center=(popup_width // 2, popup_height // 2 - 20))
    popup_surface.blit(text, text_rect)

    if show_save:
        yes_button = pygame.Rect(popup_width - 280, popup_height - 50, 100, 30)
        pygame.draw.rect(popup_surface, WHITE, yes_button)
        pygame.draw.rect(popup_surface, BLACK, yes_button, 2)
        yes_text = font.render("Save log", True, BLACK)
        yes_text_rect = yes_text.get_rect(center=yes_button.center)
        popup_surface.blit(yes_text, yes_text_rect)

    no_button = pygame.Rect(popup_width - 120, popup_height - 50, 100, 30)
    pygame.draw.rect(popup_surface, WHITE, no_button)
    pygame.draw.rect(popup_surface, BLACK, no_button, 2)
    no_text = font.render("Quit", True, BLACK)
    no_text_rect = no_text.get_rect(center=no_button.center)
    popup_surface.blit(no_text, no_text_rect)

    menu_button = pygame.Rect(20, popup_height - 50, 100, 30)
    pygame.draw.rect(popup_surface, WHITE, menu_button)
    pygame.draw.rect(popup_surface, BLACK, menu_button, 2)
    menu_text = font.render("Menu", True, BLACK)
    menu_text_rect = menu_text.get_rect(center=menu_button.center)
    popup_surface.blit(menu_text, menu_text_rect)

    screen.blit(popup_surface, (popup_x, popup_y))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Convert mouse_pos to be relative to the popup surface
                mouse_pos_rel = (mouse_pos[0] - popup_x, mouse_pos[1] - popup_y)

                if yes_button is not None:
                    if yes_button.collidepoint(mouse_pos_rel):
                        # Save button clicked
                        file_dialog(config_list)
                        return True # default behaviour instead of 'none'

                if no_button.collidepoint(mouse_pos_rel):
                    return False

                if menu_button.collidepoint(mouse_pos_rel):
                    return True


        pygame.display.update()


# Step 6: Create the function to handle the popup and user input
def handle_popup(config):
    show_popup(config)
    global yes_button
    global no_button
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return

            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if yes_button.collidepoint(mouse_pos):
                    # Save button clicked
                    file_dialog(config)

                if no_button.collidepoint(mouse_pos):
                    # No thanks button clicked
                    return

        pygame.display.update()


# Step 7: Create the file save dialog function
def file_dialog(config_list: list):
    # Add your file save dialog code here
    # This is just a placeholder
    path = save()
    if path:
        logger = Logger()
        path = path + ".csv"
        logger.log_csv(configs=config_list, full_path=path)


# Step 8: Run the game loop
def run_popup(config):
    # pygame.init()

    # Step 2: Set up the display window
    screen = pygame.display.set_mode((400, 200))
    pygame.display.set_caption("Popup Example")

    # Step 3: Define colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


    # handle_popup(config)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if event.key == K_SPACE:
                    handle_popup(config)

        pygame.display.update()

# run_popup(None)
