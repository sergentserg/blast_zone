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

class Tree(SpriteW):
    image = 'treeGreen_small.png'
    def __init__(self, x, y, groups):
        SpriteW.__init__(self, x, y, Tree.image,
                        (groups['all'], groups['obstacles']))
        self._layer = cfg.ITEM_LAYER
