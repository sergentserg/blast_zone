import pygame as pg

class SpriteW(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
