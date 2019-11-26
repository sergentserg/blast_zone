from .barrel import Barrel

class PowerBarrel(Barrel):
    def __init__(self, x, y, groups):
        img_file = "specialBarrel1_outline.png"
        Barrel.__init__(self, x, y, img_file, groups)
