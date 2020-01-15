from .barrel import Barrel

class ColorBarrel(Barrel):
    def __init__(self, x, y, color, type, groups):
        """ type  is "standard", "power", or "rapid" """
        img_file = f"tank{color}_barrel{Barrel.TYPES[type]}.png"
        Barrel.__init__(self, x, y, type, img_file, groups)
        self.color = color
