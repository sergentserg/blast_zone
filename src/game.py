import pygame as pg

import src.config as cfg
from src.game_state import GameNotPlayingState
from src.ui.game_ui import GameUI
from src.input.input_manager import InputManager


class Game:
    def __init__(self):
        """
        Initializes resources such as the screen, clock, InputManager, UI, initial
        behavior state, and flags.

        """

        self.screen = pg.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        pg.display.set_caption(cfg.TITLE)
        self.clock = pg.time.Clock()

        self.input_manager = InputManager(self)
        self.ui = GameUI(self)

        self.state = GameNotPlayingState(self)
        self.state.enter()

        self.paused = False

        # Game Loop Flag.
        self.running = True

    def set_state(self, new_state):
        """ Handles the transition from self.state into new_state """

        self.state.exit()
        self.state = new_state
        self.state.enter()

    def run(self):
        """
        Runs game loop: caps frame rate, processes inputs, updates sprites,
        and draws.

        """

        self.dt = self.clock.tick(cfg.FPS) / 1000
        self._process_events()
        self._update(self.dt)
        self._draw()

    def _process_events(self):
        """
        Processes events depending on the state, and delegates input handling to
        the input manager.

        """

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            self.state.process_events(event)
        self.input_manager.handle_inputs()

    def _update(self, dt):
        """  update(): Updates sprites in every group """
        self.state.update(dt)

    def _draw(self):
        """ Clears screen and redraws all sprites depending on the state. """
        # Clear the screen.
        self.screen.fill(cfg.BLACK)

        # Draw all sprites.
        self.state.draw()

        title = f"{cfg.TITLE} FPS: {int(self.clock.get_fps())}"
        pg.display.set_caption(title)
        pg.display.flip()

    def quit(self):
        """ Shuts down pygame subsystems. """
        pg.quit()
