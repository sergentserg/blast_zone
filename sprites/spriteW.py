import pygame as pg
from sprite_loader.py import spritesheet1

class SpriteW(pg.sprite.Sprite):
    def __init__(self, x, y, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = spritesheet1.get_image(filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
