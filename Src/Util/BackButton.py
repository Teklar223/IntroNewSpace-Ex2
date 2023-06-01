import pygame

class BackButton:
    def __init__(self, position, image):
        self.position = position
        self.image = image  # Replace with your button image
        self.rect = self.image.get_rect(topleft=position)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)