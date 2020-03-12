from random import random
import pygame as pg

from src.sprites.barrels.barrel import Barrel
from src.sprites.misc.obstacles import Barricade
import src.config as cfg

class SpecialBarrel(Barrel):
    def __init__(self, x, y, type, style, groups):
        """ type  is "standard", "power", or "rapid" """
        img_file = f'specialBarrel{style}.png'
        Barrel.__init__(self, x, y, type, img_file, groups)
        self.id = id(self)
        bar = Barricade(*self.rect.center, groups)
        bar.id = self.id
