import pygame as pg
vec = pg.math.Vector2

class Movable:
    def __init__(self, x, y):
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def move(self, dt):
        self.vel += self.acc * dt
        self.pos += (self.vel * dt) + (0.5 * self.acc * dt**2)
        self.rect.center = self.pos
