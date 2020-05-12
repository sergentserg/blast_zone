import pygame as pg

from src.sprites.spriteW import SpriteW
import src.config as cfg

class BoundaryWall(pg.sprite.Sprite):
    def __init__(self, x, y, width, height, groups):
        pg.sprite.Sprite.__init__(self, (groups['all'], groups['obstacles']))
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hit_rect = self.rect
        self.id = -1

class Tree(SpriteW):
    _IMAGE = 'treeGreen_small.png'
    def __init__(self, x, y, groups):
        SpriteW.__init__(self, x, y, Tree._IMAGE,
                        (groups['all'], groups['obstacles']))
        self._layer = cfg.ITEM_LAYER

class Barricade(SpriteW):
    _IMAGE = 'barricadeMetal.png'
    def __init__(self, x, y, groups):
        SpriteW.__init__(self, x, y, Barricade._IMAGE,
                                    (groups['all'], groups['obstacles']))
        # Shrink hitbox and recenter
        self.image = pg.transform.scale(self.image,
                                    (4 * self.rect.w // 5, 4 * self.rect.h // 5))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = self.rect
