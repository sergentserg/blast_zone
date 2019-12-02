from ..spriteW import SpriteW
from src.sprites.barrels.Barrel import Barrel
from src.sprites.interfaces.movable import Movable
from src.sprites.interfaces.rotatable import Rotatable

class Tank(SpriteW, Movable, Rotatable):
    def __init__(self, x, y, img_file, groups):
        SpriteW.__init__(self, x, y, img_file, groups)
        Movable.__init__(self, x, y)
        Rotatable.__init__(self)
        self.barrel = None

    def update(self, dt):
        # Call move? Should move check for collisions/out of bounds?
        pass

    # Override rotate to call barrel's rotate? Maybe, maybe not
    def rotate(self, dt):
        pass

    def __spawn_tracks(self):
        pass

    # Override kill to call barrel's kill?
    def kill(self):
        self.barrel.kill()
        self.barrel = None
        super().kill()
