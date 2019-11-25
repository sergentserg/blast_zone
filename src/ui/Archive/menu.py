from .buttons import Button
import pygame as pg
#from .game_text import text_renderer

class Menu:
    def __init__(self, x, y, w, h):
        # Create surface for the menu
        self.img = pg.Surface((w, h))
        self.img.fill((0, 0, 255))
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.buttons = []
        self.init_buttons()
        # Create a list of buttons
        # Blit the surface of the button relative onto to the menu surface

    def init_buttons(self):
        button_text = ["start", "options", "mute"]
        b_w, b_h = 300, 150 #button width, button height
        spacing = 40 #vertical spacing of buttons
        allButtonsHeight = (spacing*3+b_h*3)
        buttons_midtop = (self.rect.centerx - int(0.5*b_w), self.rect.centery - int(allButtonsHeight/2))
        buttons_topleft = (buttons_midtop[0], buttons_midtop[1])

        for foo in range(len(button_text)):
            buttons123 = Button(buttons_topleft[0],buttons_topleft[1] + foo*(spacing+50),
                                                b_w, b_h , button_text[foo])
            #Add buttons to list
            self.buttons.append(buttons123)
            #Display buttons on menu
            self.img.blit(buttons123.img, buttons123.rect)
