import pygame

class BackButton:
    def __init__(self, position, image, scale = (25,25)):
        self.position = position
        self.image = image 
        self.image = pygame.transform.scale(self.image, scale)
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)