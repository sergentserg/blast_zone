import pygame as pg
from src.settings import BLACK
from src.utility.sprite_loader import img_loader

class SpriteW(pg.sprite.Sprite):
    def __init__(self, x, y, img_file, groups):
        pg.sprite.Sprite.__init__(self, groups)
        self.image = img_loader.get_image(img_file)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
