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
        self.barrel_offset = int(self.rect.h/3)
        self.vel = (45, 55)
        self.rot_speed = 60

    def set_barrel(self, barrel):
        pass

    def rotate_barrel(self, aim_vec, dt):
        pointing = aim_vec - vec(*self.rect.center)
        self.barrel.rect.center = vec(*self.rect.center) + vec(self.barrel_offset, 0).rotate(pointing.angle_to(vec(1, 0)))
        self.barrel.rot = self.rot
        self.barrel.rotate(dt)

    def update(self, dt):
        # Call move? Should move check for collisions/out of bounds?
        self.rotate(dt)
        self.move(dt)



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
