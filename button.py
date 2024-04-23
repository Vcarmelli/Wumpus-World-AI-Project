
import pygame as pg

pg.font.init()
btn_txt = pg.font.SysFont('Arial Black', 23)

class Button:
    def __init__(self, xy, text_input, btn_color, hover_color):
        self.x_pos = xy[0]
        self.y_pos = xy[1]
        self.text_input = text_input
        self.text = btn_txt.render(self.text_input, True, 'black')
        self.rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.btn_color = btn_color
        self.hover_color = hover_color

    def draw_button(self, screen):
        pg.draw.rect(screen, self.btn_color, pg.Rect.inflate(self.rect, 30, 25))
        screen.blit(self.text, self.rect)

    def draw_button_transparent(self, screen):
        shape = pg.Surface(self.rect.size, pg.SRCALPHA)
        pg.draw.rect(shape, self.btn_color, shape.get_rect())
        alpha_surface = pg.Surface(self.rect.size, pg.SRCALPHA)        
        alpha_surface.blit(screen, (0, 0), special_flags=pg.BLEND_RGBA_MULT)
        screen.blit(self.text, self.rect)

    def click_button(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def update_color(self, pos):
        if pos[0] in range(self.rect.left, self.rect.right) and pos[1] in range(self.rect.top, self.rect.bottom):
            self.text = btn_txt.render(self.text_input, True, self.hover_color)
        else:
            self.text = btn_txt.render(self.text_input, True, 'white')