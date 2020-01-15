from os import path
import pygame as pg

from src.settings import IMG_DIR, SCREEN_WIDTH, SCREEN_HEIGHT
from src.levels.level import Level
from src.entities.player_ctrl import PlayerCtrl

class GameNotPlayingState:
    def __init__(self, game):
        self.game = game

    def enter(self):
        """ Creates splash surface, as well as the main menu object from UI """

        self.splash_img = pg.image.load(path.join(IMG_DIR, "Sample.png")).convert_alpha()
        self.splash_img = pg.transform.scale(self.splash_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.splash_rect = self.splash_img.get_rect()
        self.game.ui.main_menu()

    def exit(self):
        """ Gets rid of topmost menu. Shows loading screen?"""

        self.game.ui.pop_menu()
        self.game = None

    def process_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                pass
            elif event.key == pg.K_DOWN:
                pass
            elif event.key == pg.K_LEFT:
                pass
            elif event.key == pg.K_DOWN:
                pass

    def handle_keys(self, active_bindings):
        pass

    def handle_mouse(self, mouse_state, mouse_x, mouse_y):
        pass

    def update(self, dt):
        pass

    def draw(self):
        self.game.screen.blit(self.splash_img, self.splash_rect)
        self.game.ui.draw(self.game.screen)

class GamePlayingState:
    def __init__(self, game):
        self.game = game

    def enter(self):
        self.create_level()

    def exit(self):
        # Save score or something
        # Kill all sprites?
        self.level = None
        self.player = None

    def create_level(self):
        self.player = PlayerCtrl()
        self.level = Level('level_1.tmx', self.player)

    def process_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_p:
                self.toggle_pause()

    def toggle_pause(self):
        self.game.paused = not self.game.paused
        self.game.ui.pause(self.game.paused)

    def handle_keys(self, active_bindings):
        if not self.game.paused:
            self.player.handle_keys(active_bindings)

    def handle_mouse(self, mouse_state, mouse_x, mouse_y):
        if not self.game.paused:
            self.player.handle_mouse(mouse_state, mouse_x, mouse_y)

    def update(self, dt):
        if not self.game.paused:
            self.level.update(dt)

    def draw(self):
        self.level.draw(self.game.screen)
        self.game.ui.draw(self.game.screen)
