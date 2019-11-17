import pygame as pg
from ..img.sprite_loader import img_loader

class SpriteW(pg.sprite.Sprite):
    def __init__(self, x, y, filename):
        pg.sprite.Sprite.__init__(self)
        self.image = img_loader.get_image(filename)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
