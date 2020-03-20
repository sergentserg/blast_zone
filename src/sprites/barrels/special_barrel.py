from random import random
import pygame as pg

from src.sprites.barrels.barrel import Barrel
from src.sprites.misc.obstacles import Barricade
import src.config as cfg

vec = pg.math.Vector2

class SpecialBarrel(Barrel):
    def __init__(self, parent, offset, type, style, groups):
        """ type  is "standard", "power", or "rapid" """
        img_file = f'specialBarrel{style}.png'
        Barrel.__init__(self, parent, offset, img_file, groups, type=type)


class Turret(Barricade):
    def __init__(self, x, y, type, style, groups):
        Barricade.__init__(self, x, y, groups)
        offset = vec(0, 0)
        self.barrel = SpecialBarrel(self, offset, type, style, groups)
        self.id = id(self)
        self.barrel.id = self.id

    def fire(self, dir):
        self.barrel.rot = dir
        self.barrel.rotate()
        if self.barrel.ammo_count <= 0:
            self.barrel.reload_ammo()
        self.barrel.fire()
