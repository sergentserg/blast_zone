import pygame as pg
from src.settings import BLACK
from src.utility.sprite_loader import img_loader

class SpriteW(pg.sprite.Sprite):
    def __init__(self, x, y, image, groups):
        pg.sprite.Sprite.__init__(self, groups)
        self.image = img_loader.get_image(image)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
