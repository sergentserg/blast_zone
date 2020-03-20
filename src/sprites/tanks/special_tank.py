from random import random
import pygame as pg

from src.sprites.tanks.tank import Tank
from src.sprites.barrels.special_barrel import SpecialBarrel
import src.config as cfg

class SpecialTank(Tank):
    def __init__(self, x, y, type, style, groups):
        img_file = f'tankBody{style}.png'
        Tank.__init__(self, x, y, img_file, groups)
        self.barrel  = SpecialBarrel(x, y, type, style, groups)
        self.id = id(self)
        self.barrel.id = self.id
