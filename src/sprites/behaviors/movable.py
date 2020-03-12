import pygame as pg

import src.config as cfg
vec = pg.math.Vector2


class Movable:
    def __init__(self, x, y):
        self.pos = vec(x, y)
        self.vel = vec(0, 0)

    def move(self, walls_grp, dt):
        displacement = self.vel * dt
        self._handle_walls(displacement, walls_grp)

    # default, meant to be overriden.
    def _handle_walls(self, displacement, walls_grp):
        self.pos += displacement
        self.rect.center = self.pos
        self.hit_rect.center = self.pos


class MovableNonlinear(Movable):
    SPEED_CUTOFF = 100
    def __init__(self, x, y):
        Movable.__init__(self, x, y)
        self.acc = vec(0, 0)

    # Override.
    def move(self, walls_grp, dt):
        # Simulate friction.
        self.acc -= 4*self.vel

        # Effect kinematic equations.
        self.vel += self.acc * dt
        if self.vel.length_squared() < self.SPEED_CUTOFF:
            self.vel = vec(0, 0)
        else:
            displacement = (self.vel * dt) + (0.5 * self.acc * dt**2)
            self._handle_walls(displacement, walls_grp)
