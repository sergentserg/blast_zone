from .tank import Tank
from src.sprites.barrels.color_barrel  import ColorBarrel

class ColorTank(Tank):
    BLUE, DARK, GREEN, SAND, RED =  "blue", "dark", "green", "sand", "red"
    def __init__(self, x, y, color, groups):
        img_file = "tankBody_{0}_outline.png".format(color)
        Tank.__init__(self, x, y, img_file, groups)
        self.barrel  = ColorBarrel(x, y, color.capitalize(), "standard", groups)
        # self.barrel  = ColorBarrel(x, y + int(self.rect.h/3) , color.capitalize(), "standard", groups)
