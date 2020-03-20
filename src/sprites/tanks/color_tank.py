from src.sprites.tanks.tank import Tank
from src.sprites.barrels.color_barrel import ColorBarrel

class ColorTank(Tank):
    def __init__(self, x, y, color, groups):
        img_file = f"tankBody_{color}_outline.png"
        Tank.__init__(self, x, y, img_file, groups)
        offset = int(self.hit_rect.height/3)
        self.barrels.append(ColorBarrel(self, offset, color.capitalize(), groups))
        self.id = id(self)
        for barrel in self.barrels:
            barrel.id = self.id
