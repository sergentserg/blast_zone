from .menu import Menu
from src.settings import WHITE

class PauseMenu(Menu):
    def __init__(self, groups, game):
        Menu.__init__(self, "Game Paused", groups)
        self.game = game
        btn_images = ["blue_button04.png", "blue_button02.png", "blue_button03.png"]
        self._add_button(groups=groups,images=btn_images,
                        action=self.resume,
                        text='Continue', size=24, color=WHITE)

        self._add_button(groups=groups, images=btn_images,
                        action = lambda: print("Restart the game"),
                        text='Restart', size=24, color=WHITE)

        self._add_button(groups=groups, images=btn_images,
                        action = lambda: print("Quit the game"),
                        text='Main Menu', size=24, color=WHITE)

        self._make_menu()

    def resume(self):
        self.game.state.toggle_pause()
