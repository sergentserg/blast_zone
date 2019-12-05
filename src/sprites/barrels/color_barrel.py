from .barrel import Barrel

# my_blue_barrel = ColorBarrel(0, 0, ColorBarrel.RED, "standard", )
class ColorBarrel(Barrel):
    TYPE = {"standard": 1, "power": 2, "rapid": 3}
    def __init__(self, x, y, color, type, groups):
        """ type  is "standard", "power", or "rapid" """
        img_file = "tank{0}_barrel{1}.png".format(color, self.TYPE[type])
        Barrel.__init__(self, x, y, type, img_file, groups)
        self.color = color
