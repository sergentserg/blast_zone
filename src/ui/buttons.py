#Create a class for user inputs
import pygame as pg
from .game_text import text_renderer

class Button:
    def __init__(self, x, y, w, h, button_text):
        # The border
        border_surf = pg.Surface((w+2, h+2))
        border_surf.fill((0, 255, 0))
        # The inner surface
        fill_surf = pg.Surface((w, h))
        fill_surf.fill((255, 0, 0))
        fill_rect = fill_surf.get_rect()
        fill_rect.center = border_surf.get_rect().center
        border_surf.blit(fill_surf, fill_rect)
        self.img = border_surf
        text_renderer.render(self.img, button_text, 10, (255, 255, 255), 'calibri')
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        # print("Button rect is: {0}".format(self.rect))

        # border_rect = pg.draw.rect(self.img, (255, 255, 255), self.rect, -1000)
        # print("the border rect is: {0}".format(border_rect))

    def handle_input(self, mouse_X, mouse_Y, dt):
        if (self.rect.x <= mouse_X <= self.rect.x + self.rect.w) and (
                    self.rect.y <= mouse_Y <= self.rect.y + self.rect.h):
            print("Clicked at {0}".format(dt))



# button1 is an instance of the Button class/ button1 is an object of type Button
# button1 = Button()

# # GameOverButton inherits from Button/ GameOverButton subclasses Button
# class GameOverButton(Button):
#     def __init__(self, x, y):
#         Button.__init__(x, y)
