#Create a class for user inputs
import pygame as pg
from src.utility.game_text import text_renderer
from src.sprites.animated_sprite import AnimatedSprite

class Button(AnimatedSprite):
    def __init__(self, x, y, action, text, filenames):
        AnimatedSprite.__init__(self, x, y, filenames)
        text_renderer.render(self.img, text['text'], text['size'], text['color'])
        self.action = action

    def handle_mouse(self, mouse_x, mouse_y, dt, clicked):
        # is mouse over button?
        if (self.rect.x <= mouse_x <= self.rect.x + self.rect.w) and (
                    self.rect.y <= mouse_y <= self.rect.y + self.rect.h):
            if clicked:
                self.action['execute']()
                self.update_anim(dt)
