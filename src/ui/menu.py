import pygame as pg
from .button import Button
import src.settings as cfg
import src.input.input_state as input_state
from src.utility.game_text import text_renderer
from src.sprites.spriteW import SpriteW

class Menu(SpriteW):
    BUTTON_PADDING = 15
    TITLE_SIZE = 30
    def __init__(self, title, groups):
        SpriteW.__init__(self, 0, 0, "blue_panel.png", groups)
        self.title = title
        self.buttons = []

    def _make_menu(self, num_columns=1):
        # Resize menu surface
        width = (self.buttons[0].rect.w + Menu.BUTTON_PADDING * 2) * num_columns
        height = (self.buttons[0].rect.h + Menu.BUTTON_PADDING) * (len(self.buttons) + 1)
        self.image = pg.transform.scale(self.image, (width, height))
        self.image.set_colorkey(cfg.BLACK)
        # Recenter menu surface
        self.rect = self.image.get_rect()
        self.rect.center = (cfg.SCREEN_WIDTH / 2, cfg.SCREEN_HEIGHT / 2)
        # Render menu title
        text_renderer.render_pos(self.image, x=self.rect.w/2,
                                    y=2*Menu.BUTTON_PADDING,
                                    text=self.title, size=Menu.TITLE_SIZE, color=cfg.WHITE)
        # Position buttons
        menu_offset = (Menu.TITLE_SIZE*2)  + self.rect.top
        for i in range(len(self.buttons)):
            # 36 Points to pixels conversion mult by 4/3
            self.buttons[i].rect.top =  menu_offset + i * (self.buttons[i].rect.h + Menu.BUTTON_PADDING)
            self.buttons[i].rect.centerx = cfg.SCREEN_WIDTH / 2

    def _add_button(self, groups, images, action, **text):
        button = Button(groups, images, action, **text)
        self.buttons.append(button)

    def handle_mouse(self, mouse_state, mouse_x, mouse_y):
        for button in self.buttons:
            button.handle_mouse(mouse_state, mouse_x, mouse_y)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        for button in self.buttons:
            surface.blit(button.image, button.rect)

    def kill(self):
        for button in self.buttons:
            button.kill()
        super().kill()
