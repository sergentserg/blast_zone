from .barrel import Barrel

class ColorBarrel(Barrel):
    BLUE, DARK, GREEN, DARK, RED = "Blue", "Dark", "Green", "Dark", "Red"
    TYPE = {"standard": 1, "power": 2, "rapid": 3}
    def __init__(self, x, y, color, type, groups):
        """ type  is "standard", "power", or "rapid" """
        img_file = "tank{0}_barrel{1}.png".format(color, ColorBarrel.TYPE.get(type))
        Barrel.__init__(self, x, y, type, img_file, groups)
        self.color = color
