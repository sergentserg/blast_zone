from src.sprites.barrels.barrel import Barrel

class ColorBarrel(Barrel):
    def __init__(self, parent, offset, color, groups):
        """ types are: "standard", "power", or "rapid" """
        type = self.TYPES["standard"]
        img_file = f"tank{color}_barrel{type}.png"
        Barrel.__init__(self, parent, offset, img_file, groups)
        self.color = color
        self.rect.midtop = parent.rect.center
