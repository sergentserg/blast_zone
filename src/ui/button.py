import pygame as pg
from ..input.input_manager import input_handler
class Button:
    def __init__(self, width, height):
        self.img = pg.Surface((width, height))
        self.img.fill((255, 0, 0))
        self.rect = self.img.get_rect()
        self.rect.x  = 20
        self.rect.y = 20

    def update(self):
        mouse_buttons = pg.mouse.get_pressed()
        #if button 1 is pressed
        if mouse_buttons[0]:
            mouse_x, mouse_y = pg.mouse.get_pos()
            if (self.rect.x < mouse_x < self.rect.x + self.rect.width) and (
                        self.rect.y < mouse_y < self.rect.y + self.rect.height):
                print("Click inside!")
            else:
                print("Clicked ouside")
