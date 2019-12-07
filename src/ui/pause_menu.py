from .menu import Menu
from src.settings import WHITE

class PauseMenu(Menu):
    def __init__(self):
        Menu.__init__(self, "Game Paused")
        btn_imgs = ["blue_button04.png", "blue_button02.png", "blue_button03.png"]
        self.add_button(x=0, y=0, images=btn_images,
                        lambda: print("Resume the game"),
                        text='Continue', size=24, color=WHITE)

        self.add_button(x=0, y=0, images=btn_images,
                        lambda: print("Restart the game"),
                        text='Restart', size=24, color=WHITE)

        self.add_button(x=0, y=0, images=btn_images,
                        lambda: print("Quit the game"),
                        text='Quit', size=24, color=WHITE)
