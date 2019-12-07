from .menu import Menu
from src.settings import WHITE

class MainMenu(Menu):
    def __init__(self):
        Menu.__init__(self, "Main Menu")
        btn_imgs = ["blue_button04.png", "blue_button02.png", "blue_button03.png"]
        self.add_button(x=0, y=0, images=btn_images,
                        lambda: print("Resume the game"),
                        text='Play', size=24, color=WHITE)

        self.add_button(x=0, y=0, images=btn_images,
                        lambda: print("Restart the game"),
                        text='Controls', size=24, color=WHITE)
