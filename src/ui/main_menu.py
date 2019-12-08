from .menu import Menu
from src.settings import WHITE

class MainMenu(Menu):
    def __init__(self, groups):
        Menu.__init__(self, "Game Paused", groups)
        btn_images = ["blue_button04.png", "blue_button02.png", "blue_button03.png"]
        self.add_button(x=0, y=0, images=btn_images,
                        lambda: print("Resume the game"),
                        text='Play', size=24, color=WHITE)

        self.add_button(x=0, y=0, images=btn_images,
                        lambda: print("Restart the game"),
                        text='Controls', size=24, color=WHITE)

        self.add_button(x=0, y=0, images=btn_images,
                        lambda: print("Display menu screen"),
                        text='Credits', size=24, color=WHITE)

        self.add_button(x=0, y=0, images=btn_images,
                        lambda: print("Quit the game"),
                        text='Quit', size=24, color=WHITE)
