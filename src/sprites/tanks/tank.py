from ..spriteW import SpriteW
from src.sprites.interfaces.movable import Movable
from src.sprites.interfaces.rotatable import Rotatable
import pygame as pg
vec = pg.math.Vector2

class Tank(SpriteW, Movable, Rotatable):
    def __init__(self, x, y, img_file, groups):
        SpriteW.__init__(self, x, y, img_file, groups)
        Movable.__init__(self, x, y)
        Rotatable.__init__(self)
        self.barrel = None
        self.vel = (0, 0)
        self.rot = 0

    def set_barrel(self, barrel):
        pass

    def update(self, dt):
        # Call move? Should move check for collisions/out of bounds?
        self.rotate(dt)
        self.move(dt)
        self.barrel.rect.midtop = vec(*self.rect.center).rotate(-self.rot)
        self.barrel.rot = 0
        self.barrel.rotate(dt)


    # Override rotate to call barrel's rotate? Maybe, maybe not
    def rotate(self, dt):
        self.barrel.rotate(dt)
        super().rotate(dt)

    def __spawn_tracks(self):
        pass

    # Override kill to call barrel's kill?
    def kill(self):
        self.barrel.kill()
        super().kill()
