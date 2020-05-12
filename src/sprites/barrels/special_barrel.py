from random import random
import pygame as pg

from src.sprites.barrels.barrel import Barrel
from src.sprites.misc.obstacles import Barricade
from src.sprites.behaviors.damageable import Damageable
import src.config as cfg

vec = pg.math.Vector2


class SpecialBarrel(Barrel):
    def __init__(self, parent, offset, type, style, groups):
        """ type  is "standard", "power", or "rapid" """
        img_file = f'specialBarrel{style}.png'
        Barrel.__init__(self, parent, offset, img_file, groups, type=type)


class Turret(Barricade, Damageable):
    def __init__(self, x, y, type, style, groups):
        Barricade.__init__(self, x, y, groups)
        Damageable.__init__(self, self.hit_rect)
        groups['damageable'].add(self)
        self.barrel = SpecialBarrel(self, vec(0, 0), type, style, groups)
        # Bullets spawned by turret won't hurt turret, but hurts other sprites.
        self.id = id(self)
        self.barrel.id = self.id

    def kill(self):
        self.barrel.kill()
        super().kill()

    def fire(self, dir):
        self.barrel.rot = dir
        self.barrel.rotate()
        if self.barrel.ammo_count <= 0:
            self.barrel.reload()
        self.barrel.fire()
