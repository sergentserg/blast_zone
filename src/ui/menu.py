import pygame as pg
from .buttons import Button
import src.settings as cfg
import src.input.input_manager as input_manager

class Menu:
    def __init__(self):
        self.buttons = []
        self.__init_buttons()

    def __init_buttons(self):
        btn_txt = {'text': 'Button 1', 'size': 24, 'color': cfg.WHITE}
        btn_imgs = ["blue_button04.png", "blue_button03.png"]
        button1 = Button(cfg.SCREEN_WIDTH/2, cfg.SCREEN_HEIGHT/2,
                            {'execute': lambda: print("Click!")},btn_txt, btn_imgs)
        self.buttons.append(button1)

    def handle_mouse(self, dt, mouse_state):
        mouse_x, mouse_y = pg.mouse.get_pos()
        for button in self.buttons:
            button.handle_mouse(mouse_x, mouse_y, dt, mouse_state)

    def draw(self, surface):
        for button in self.buttons:
            surface.blit(button.img, button.rect)
