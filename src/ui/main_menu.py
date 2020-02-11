from src.ui.menu import Menu
import src.config as cfg
from src.game_state import GamePlayingState

class MainMenu(Menu):
    def __init__(self, groups, game):
        Menu.__init__(self, "Main Menu", groups)

        self.game = game

        btn_images = ["blue_button04.png", "blue_button02.png", "blue_button03.png"]
        self._add_button(groups=groups, images=btn_images,
                        action=self.play_game,
                        text='Play', size=24, color=cfg.WHITE)

        self._add_button(groups=groups, images=btn_images,
                        action=lambda: print("Choose your controls"),
                        text='Controls', size=24, color=cfg.WHITE)

        self._add_button(groups=groups, images=btn_images,
                        action=lambda: print("Display credits"),
                        text='Credits', size=24, color=cfg.WHITE)

        self._add_button(groups=groups, images=btn_images,
                        action=lambda: self.quit_game(),
                        text='Quit', size=24, color=cfg.WHITE)
        self._make_menu()

    def play_game(self):
        self.game.set_state(GamePlayingState(self.game))
        self.game.ui.pop_menu()

    def quit_game(self):
        self.game.running = False
