from src.sprites.tanks.tank import Tank
from src.sprites.barrels.color_barrel import ColorBarrel

class ColorTank(Tank):
    def __init__(self, x, y, color, groups):
        img_file = f"tankBody_{color}_outline.png"
        Tank.__init__(self, x, y, img_file, groups)
        offset = int(self.hit_rect.height/3)
        self.color = color.capitalize()
        self.barrels.append(ColorBarrel(self, offset, self.color, groups))
        self.max_ammo = self.barrels[0].get_ammo_count()
        self.id = id(self)
        for barrel in self.barrels:
            barrel.id = self.id
