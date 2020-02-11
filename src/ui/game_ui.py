import pygame as pg

from src.ui.main_menu import MainMenu
from src.ui.pause_menu import PauseMenu

class GameUI:
    def __init__(self, game):
        self.game = game
        self.ui_sprites = pg.sprite.Group()
        self.menus = []

    def handle_input(self, active_bindings, mouse_state, mouse_x, mouse_y):
        self.handle_keys(active_bindings)
        self.handle_mouse(mouse_state, mouse_x, mouse_y)

    def handle_keys(self, active_bindings):
        pass

    def handle_mouse(self, mouse_state, mouse_x, mouse_y):
        if self.menus:
            self.menus[-1].handle_mouse(mouse_state, mouse_x, mouse_y)

    def toggle_pause(self):
        self.game.paused = not self.game.paused
        if self.game.paused:
            self.menus.append(PauseMenu(self.ui_sprites, self.game))
        else:
            self.pop_menu()

    def main_menu(self):
        self.menus.append(MainMenu(self.ui_sprites, self.game))

    def pop_menu(self):
        # Remove topmost menu
        if self.menus:
            self.menus[-1].kill()
            del self.menus[-1]

    def draw(self, surface):
        self.ui_sprites.draw(surface)
