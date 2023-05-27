import pygame as pg

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

class InputBox:

    def __init__(self, x, y, w, h, text='', permatext = 'HELLO: '):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.permatext = permatext
        self.text_to_render = self.permatext + self.text
        self.txt_surface = FONT.render(self.text_to_render, True, self.color)
        self.active = False

    def handle_event(self, event, set_method = None):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                if set_method:
                    set_method(key = self.permatext, value = self.text)
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.text_to_render = self.permatext + self.text
                self.txt_surface = FONT.render(self.text_to_render, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        self.rect.w = max(200, self.txt_surface.get_width() + 10)

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)

def to_pg_coords(x, y, canvas_height):
    _x = x
    _y = canvas_height - y
    return _x, _y

def to_pg_angle(angle):
    return 180 + angle 