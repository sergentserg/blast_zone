import pygame as pg
vec = pg.math.Vector2

class Movable:
    def __init__(self, x, y):
        self.pos = vec(x, y)
        self.vel = vec(0, 0)

    def move(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos

class MovableNonlinear(Movable):
    SPEED_CUTOFF = 100
    def __init__(self, x, y):
        Movable.__init__(self, x, y)
        self.acc = vec(0, 0)

    def move(self, dt):
        self.acc -= 4*self.vel
        self.vel += self.acc * dt
        self.pos += (self.vel * dt) + (0.5 * self.acc * dt**2)
        self.rect.center = self.pos

        if self.vel.length_squared() < self.SPEED_CUTOFF:
            self.vel = vec(0, 0)
