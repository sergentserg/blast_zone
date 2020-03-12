import pygame as pg

import src.config as cfg
from src.sprites.barrels.special_barrel import SpecialBarrel

vec = pg.math.Vector2

class TurretCtrl:
    _DETECT_RADIUS = (cfg.SCREEN_WIDTH ** 2 + cfg.SCREEN_WIDTH ** 2) / 4
    def __init__(self, x, y, type, style, groups):
        self.barrel = SpecialBarrel(x, y, type, style, groups)
        # Assigned immediately after creation.
        self.target = None

    def update(self, dt):
        if self.target.alive():
            separation = self.target.pos - vec(*self.barrel.rect.center)
            if separation.length_squared() > TurretCtrl._DETECT_RADIUS:
                pass
            else:
                dir = separation.angle_to(vec(1, 0))
                self.barrel.rot = dir
                self.barrel.rotate()
                if self.barrel.ammo_count <= 0:
                    self.barrel.reload_ammo()
                self.barrel.fire()
