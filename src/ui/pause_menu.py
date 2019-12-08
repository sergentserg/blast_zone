from .menu import Menu
from src.settings import WHITE

class PauseMenu(Menu):
    def __init__(self, groups):
        Menu.__init__(self, "Game Paused", groups)
        btn_images = ["blue_button04.png", "blue_button02.png", "blue_button03.png"]
        self._add_button(x=0, y=0, groups=groups,images=btn_images,
                        action= lambda: print("Resume the game"),
                        text='Continue', size=24, color=WHITE)

        self._add_button(x=0, y=0, groups=groups, images=btn_images,
                        action = lambda: print("Restart the game"),
                        text='Restart', size=24, color=WHITE)

        self._add_button(x=0, y=0, groups=groups, images=btn_images,
                        action = lambda: print("Quit the game"),
                        text='Quit', size=24, color=WHITE)

        self._make_menu()
