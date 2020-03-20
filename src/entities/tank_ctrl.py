import pygame as pg
vec = pg.math.Vector2

import src.config as cfg
from src.sprites.tanks.color_tank import ColorTank

class AITankCtrl:
    _DETECT_RADIUS = (cfg.SCREEN_WIDTH ** 2 + cfg.SCREEN_WIDTH ** 2) / 8
    def __init__(self, x, y, color, groups):
        self.tank = ColorTank(x, y, color, groups)
        self.target = None

    def update(self, dt):
        if not self.target.alive():
            self.tank.acc = vec(self.tank.ACCELERATION / 2, 0).rotate(-self.tank.rot)
            self.tank.rotate_barrel(self.tank.rot)
        else:
            # See if target is in range.
            separation = self.target.pos - self.tank.pos
            if separation.length_squared() > AITankCtrl._DETECT_RADIUS:
                # Idle/Patrol
                self.tank.acc = vec(self.tank.ACCELERATION / 2, 0).rotate(-self.tank.rot)
                self.tank.rotate_barrel(self.tank.rot)
            else:
                self.tank.rot = separation.angle_to(vec(1, 0))
                self.tank.acc = vec(self.tank.ACCELERATION, 0).rotate(-self.tank.rot)
                self.tank.rotate_barrel(self.tank.rot)
                self.tank.fire()
