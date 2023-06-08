import pygame

WHITE = (0, 0, 0)
DARK = (81, 81, 81)
BLACK = (0, 0, 0)

def create_dashboard(screen, width: int, height: int):
    x = width - 200
    y = 0
    dash_width = 200
    dash_height = height
    popup_surface = pygame.Surface((dash_width, dash_height))
    popup_surface.fill(WHITE)

    popup_surface = pygame.Surface((dash_width, dash_height))
    popup_surface.fill(DARK)
    pygame.draw.rect(popup_surface, WHITE, (0, 0, dash_width, dash_height), 3)
    font = pygame.font.init()
    font = pygame.font.Font(None, 24)

    screen.blit(popup_surface, (x, y))
    pygame.display.update()


# screen = pygame.display.set_mode((600, 600))
# create_dashboard(screen, 600, 600)
