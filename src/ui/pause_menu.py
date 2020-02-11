from src.ui.menu import Menu
import src.config as cfg
from src.game_state import GameNotPlayingState

class PauseMenu(Menu):
    def __init__(self, groups, game):
        Menu.__init__(self, "Game Paused", groups)
        self.game = game
        btn_images = ["blue_button04.png", "blue_button02.png", "blue_button03.png"]
        self._add_button(groups=groups,images=btn_images,
                        action=self.resume,
                        text='Continue', size=24, color=cfg.WHITE)

        self._add_button(groups=groups, images=btn_images,
                        action=self.restart,
                        text='Restart', size=24, color=cfg.WHITE)

        self._add_button(groups=groups, images=btn_images,
                        action=self.main_menu,
                        text='Main Menu', size=24, color=cfg.WHITE)

        self._make_menu()

    def resume(self):
        self.game.ui.toggle_pause()

    def restart(self):
        self.game.ui.toggle_pause()
        self.game.state.create_level()

    def main_menu(self):
        self.game.ui.toggle_pause()
        self.game.set_state(GameNotPlayingState(self.game))
