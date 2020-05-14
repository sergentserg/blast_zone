import pygame as pg

import src.config as cfg
import src.utility.game_text as gtext
from src.sprites.spriteW import SpriteW
from src.sprites.animated_sprite import AnimatedSprite
from src.input.input_state import InputState


_BTN_IMAGES = ["blue_button04.png", "blue_button02.png", "blue_button03.png"]


class UI:
    def __init__(self, game):
        self._game = game
        self._ui_sprites = pg.sprite.Group()
        self._menus = []

    def make_menu(self, title, actions, size, color):
        menu = Menu(title, actions, self._ui_sprites)
        for action in actions:
            menu.add_button(action['action'], action['text'], size, color)
        menu.render()
        self._menus.append(menu)

    def handle_input(self, active_bindings, mouse_state, mouse_x, mouse_y):
        self.handle_keys(active_bindings)
        self.handle_mouse(mouse_state, mouse_x, mouse_y)

    def handle_keys(self, active_bindings):
        pass

    def handle_mouse(self, mouse_state, mouse_x, mouse_y):
        if self._menus:
            self._menus[-1].handle_mouse(mouse_state, mouse_x, mouse_y)

    def pop_menu(self):
        # Remove topmost menu
        self._menus[-1].kill()
        del self._menus[-1]

    def clear(self):
        while self._menus:
            self.pop_menu()

    def draw(self, surface):
        self._ui_sprites.draw(surface)


class Menu(SpriteW):
    _BUTTON_PADDING = 15
    _TITLE_SIZE = 30
    IMAGE = "blue_panel.png"
    def __init__(self, title, actions, groups):
        SpriteW.__init__(self, 0, 0, Menu.IMAGE, groups)
        self._groups = groups
        self._title = title
        self.buttons = []

    def render(self):
        # Resize menu surface
        width = (self.buttons[0].rect.w + Menu._BUTTON_PADDING * 2)
        height = (self.buttons[0].rect.h + Menu._BUTTON_PADDING) * (len(self.buttons) + 1)
        self.image = pg.transform.scale(self.image, (width, height))
        self.image.set_colorkey(cfg.BLACK)

        # Recenter menu surface
        self.rect = self.image.get_rect()
        self.rect.center = (cfg.SCREEN_WIDTH / 2, cfg.SCREEN_HEIGHT / 2)

        # Render menu title
        gtext.render_pos(self.image, x=self.rect.w/2, y=2*Menu._BUTTON_PADDING,
                            text=self._title, size=Menu._TITLE_SIZE, color=cfg.WHITE)

        # Position buttons
        menu_offset = Menu._TITLE_SIZE * 2  + self.rect.top
        for i in range(len(self.buttons)):
            # 36 Points to pixels conversion mult by 4/3
            self.buttons[i].rect.top =  menu_offset + i * (self.buttons[i].rect.h + Menu._BUTTON_PADDING)
            self.buttons[i].rect.centerx = cfg.SCREEN_WIDTH / 2

    def add_button(self, action, text, size, color):
        button = Button(action, text, size, color, _BTN_IMAGES, self._groups)
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



class Button(AnimatedSprite):
    _HOVER_OFF, _HOVER_ON, _CLICKED = 0, 1, 2
    def __init__(self, action, text, size, color, img_files, groups):
        frame_info = [ {'start_frame': Button._HOVER_OFF, 'num_frames': 1},
                        {'start_frame': Button._HOVER_ON, 'num_frames': 1},
                        {'start_frame': Button._CLICKED, 'num_frames': 1}]
        AnimatedSprite.__init__(self, 0, 0, groups, img_files, frame_info)
        # Add Text to buttons.
        for i in range(len(self.images)):
            # Make a copy to safely alter image with text.
            self.images[i] = self.images[i].copy()
            gtext.render(self.images[i], text, size, color)
        # on-click button function
        self.action = action

    def handle_mouse(self, mouse_state, mouse_x, mouse_y):
        # Keep track of bottom of button
        old_bot = self.rect.bottomleft
        # check if mouse is hovering button
        if self._is_hovering(mouse_x, mouse_y):
            self.change_anim(Button._HOVER_ON)
            if mouse_state == InputState.STILL_PRESSED:
                self.change_anim(Button._CLICKED)
            elif mouse_state == InputState.JUST_RELEASED:
                # toggle-off clicked animation
                self.action()
        else:
            self.change_anim(Button._HOVER_OFF)
        # Update button position
        self.rect = self.image.get_rect()
        self.rect.bottomleft = old_bot

    def _is_hovering(self, mouse_x, mouse_y):
        if mouse_x < self.rect.left:
            return False
        if mouse_x > self.rect.right:
            return False
        if mouse_y < self.rect.top:
            return False
        if mouse_y > self.rect.bottom:
            return False
        return True
