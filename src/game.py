from os import path
import pygame as pg
import sys

import src.config as cfg
# from src.game_state import GameNotPlayingState
from src.ui import UI
from src.input.input_manager import InputManager
from src.level import Level
from src.entities.player_ctrl import PlayerCtrl
from src.utility.timer import Timer
import src.utility.game_text as gtext


class Game:
    """ The Game class effects the game loop, using state classes to determine its
        behavior.

    """

    def __init__(self):
        """ Initializes resources such as the screen, clock, InputManager, UI,
        initialbehavior state, and flags.

        """
        self._screen = pg.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        pg.display.set_caption(cfg.TITLE)

        self._clock = pg.time.Clock()

        self._input_manager = InputManager(self)
        self._ui = UI(self)

        self._state = GameNotPlayingState(self)
        self._state.enter()

        # Game Loop Flag.
        self._running = True

    @property
    def screen(self):
        return self._screen

    @property
    def clock(self):
        return self._clock

    @property
    def ui(self):
        return self._ui

    @property
    def state(self):
        return self._state

    def set_state(self, new_state):
        """ Handles the transition from self._state into new_state. """
        self._state.exit()
        self._state = new_state(self)
        self._state.enter()

    def run(self):
        """ Runs game loop: caps frame rate, processes inputs, updates sprites,
        and draws.

        """
        while True:
            self.dt = self._clock.tick(cfg.FPS) / 1000
            self._process_events()
            self._update(self.dt)
            self._draw()

    def _process_events(self):
        """ Processes events depending on the state, and delegates
        input handling tothe input manager.

        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            self._state.process_events(event)
        self._input_manager.handle_inputs()

    def _update(self, dt):
        # Updates sprites in every sprite group.
        self._state.update(dt)

    def _draw(self):
        # Clears screen and redraws all sprites depending on the state.
        self._screen.fill(cfg.BLACK)
        self._state.draw()
        title = f"{cfg.TITLE} FPS: {int(self._clock.get_fps())}"
        pg.display.set_caption(title)
        pg.display.flip()

    def quit(self):
        """ Shuts down pygame subsystems. """
        pg.quit()
        sys.exit()


class GameNotPlayingState:
    def __init__(self, game):
        self._game = game

    def enter(self):
        """ Creates splash surface, as well as the main menu object from UI. """
        splash_path = path.join(cfg.EXTRA_IMG_DIR, "Sample.png")
        self._splash_img = pg.image.load(splash_path).convert_alpha()

        dimensions = (cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
        self._splash_img = pg.transform.scale(self._splash_img, dimensions)
        self._splash_rect = self._splash_img.get_rect()
        actions = [
            {'action': lambda: self._game.set_state(GamePlayingState),'text': 'Play'},
            {'action': self._game.quit, 'text': 'Quit'},
            ]
        self._game.ui.make_menu("Main Menu", actions, 24, cfg.WHITE)

    def exit(self):
        """ Gets rid of topmost menu. Shows loading screen?"""
        self._game.ui.clear()

    def process_events(self, event):
        pass

    def handle_input(self, active_bindings, mouse_state, mouse_x, mouse_y):
        pass

    def update(self, dt):
        pass

    def draw(self):
        self._game.screen.blit(self._splash_img, self._splash_rect)
        self._game.ui.draw(self._game.screen)


class GamePlayingState:
    def __init__(self, game):
        self._game = game
        self._paused = False
        self._game_over = False

    def enter(self):
        self.create_level()

    def create_level(self):
        """ Creates a new player and restarts level sprites. """
        self._paused = False
        self._game.ui.clear()
        self._player = PlayerCtrl()
        self._level = Level('level_1.tmx', self._player, self)
        self._timer = Timer()

    def exit(self):
        # Save score or something
        self._game.ui.clear()

    def process_events(self, event):
        if not self._game_over:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    self.pause()

    def pause(self):
        if self._paused:
            self._game.ui.pop_menu()
            Timer.unpause_timers()
        else:
            actions = [
                {'action': self.pause,'text': 'Resume'},
                {'action': self.create_level, 'text': 'Restart'},
                {'action': lambda: self._game.set_state(GameNotPlayingState),'text': 'Main Menu'}
            ]
            self._game.ui.make_menu("Game Paused", actions, 24, cfg.WHITE)
            Timer.pause_timers()
        self._paused = not self._paused

    def game_over(self):
        actions = [
            {'action': lambda: self._game.set_state(GamePlayingState),'text': 'Play Again'},
            {'action': lambda: self._game.set_state(GameNotPlayingState),'text': 'Main Menu'},
            {'action': self._game.quit, 'text': 'Quit'}
        ]
        if self._player.alive():
            title = "You win!"
        else:
            title = "Game Over!"
        self._game.ui.make_menu(title, actions, 24, cfg.WHITE)
        self._timer.pause()
        self._game_over = True

    def handle_input(self, active_bindings, mouse_state, mouse_x, mouse_y):
        if not (self._paused or self._game_over):
            self._player.handle_keys(active_bindings)
            self._player.handle_mouse(mouse_state, mouse_x, mouse_y)

    def update(self, dt):
        if not self._paused:
            self._level.update(dt)

    def draw(self):
        self._level.draw(self._game.screen)
        self._game.ui.draw(self._game.screen)
        total_secs = self._timer.elapsed_time() // 1000
        mins = total_secs // 60
        secs = total_secs % 60
        gtext.render(self._game.screen, f"{mins:02d}:{secs:02d}", 24, cfg.WHITE, location='n')
