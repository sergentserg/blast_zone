import pygame as pg
from .. settings import FONT_NAMES

class TextRenderer:
    def __init__(self):
        # Load all fonts
        self.fonts = {font: pg.font.match_font(font) for font in FONT_NAMES}

    def render(self, surface, text, size, color, location = 'c', font_name = 'arial'):
        # Create font object
        font_object = pg.font.Font(self.fonts[font_name], size)

        # Create a text surface
        text_surface = font_object.render(text, True, color)
        text_rect = text_surface.get_rect()

        # Determine where to blit the text
        if location =='nw':
            dest = surface.get_rect().topleft
        elif location =='n':
            dest = surface.get_rect().midtop
        elif location =='ne':
            dest = surface.get_rect().topright
        elif location =='w':
            dest = surface.get_rect().midleft
        elif location =='c':
            dest = surface.get_rect().center
        elif location =='e':
            dest = surface.get_rect().midright
        elif location =='sw':
            dest = surface.get_rect().bottomleft
        elif location =='s':
            dest = surface.get_rect().midbottom
        elif location =='se':
            dest = surface.get_rect().bottomright

        # blit the text at dest
        text_rect.center = dest
        surface.blit(text_surface, text_rect)

text_renderer = TextRenderer()
