import pygame as pg

import src.config as cfg
from src.sprites.barrels.special_barrel import Turret

vec = pg.math.Vector2

class TurretCtrl:
    _DETECT_RADIUS = (cfg.SCREEN_WIDTH ** 2 + cfg.SCREEN_WIDTH ** 2) / 4
    def __init__(self, x, y, type, style, groups):
        self.turret = Turret(x, y, type, style, groups)
        # Assigned immediately after creation.
        self.target = None

    def update(self, dt):
        if self.target.alive():
            separation = self.target.pos - vec(*self.turret.rect.center)
            if separation.length_squared() > TurretCtrl._DETECT_RADIUS:
                pass
            else:
                dir = separation.angle_to(vec(1, 0))
                self.turret.fire(dir)
