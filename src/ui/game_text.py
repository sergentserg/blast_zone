import pygame as pg
from .. settings import FONT_NAMES

class TextRender:
    def __init__(self):
        self.fonts = {font: pg.font.match_font(font) for font in FONT_NAMES}

    def render(self, surface, text, size, color, font_name = 'arial'):
        # Create font object
        font_object = pg.font.Font(self.fonts[font_name], size)

        # Create a text surface
        text_surface = font_object.render(text, True, color)
        text_rect = text_surface.get_rect()
        print("text_rect is: {0}".format(text_rect))
        #surface.top, surface.bottom, surface.right, surface.left, surface.center
        text_rect.center = surface.get_rect().center
        surface.blit(text_surface, text_rect)

text_renderer = TextRender()
