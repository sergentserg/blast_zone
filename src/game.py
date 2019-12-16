import pygame as pg

import src.settings as cfg
from src.game_state import GameNotPlayingState, GamePlayingState
from src.ui.ui import GameUI
from src.input.input_manager import InputManager

class Game:
    def __init__(self):
        """
        __init__: Initializes pygame modules and creates a screen and Clock.

        """
        # Initialize screen and clock.
        self.screen = pg.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        pg.display.set_caption(cfg.TITLE)
        self.clock = pg.time.Clock()

        self.input_manager = InputManager(self)
        self.ui = GameUI(self)

        self.state = GameNotPlayingState(self)
        self.state.enter()

        self.paused = False

        # Debug flag.
        self.debug = False
        # Game Loop Flag.
        self.running = True

    def set_state(self, new_state):
        self.state.exit()
        self.state = new_state
        self.state.enter()

    def run(self):
        """ run(): Runs game loop: caps frame rate, processes inputs,
        updates sprites, and draws.

        """
        # Used to continue game loop
        self.dt = self.clock.tick(cfg.FPS) / 1000
        self.process_events()
        self.update(self.dt)
        self.draw()

    def process_events(self):
        """ Process user-inputs from the keyboard and mouse. """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            self.state.process_events(event)
        self.input_manager.handle_inputs()

    def update(self, dt):
        """  update(): Updates sprites in every group """
        self.state.update(dt)

    def draw(self):
        """ draw(): Draws UI and game world onto screen. """
        # Clear the screen.
        self.screen.fill(cfg.BLACK)

        # Draw all sprites.
        self.state.draw()

        title = f"{cfg.TITLE} FPS: {int(self.clock.get_fps())}"
        pg.display.set_caption(title)
        pg.display.flip()

    def quit(self):
        pg.quit()
