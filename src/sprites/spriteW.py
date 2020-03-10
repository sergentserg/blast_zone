import pygame as pg

import src.config as cfg
import src.utility.sprite_loader as sprite_loader

class SpriteW(pg.sprite.Sprite):
    def __init__(self, x, y, image, groups):
        pg.sprite.Sprite.__init__(self, groups)
        self.image = sprite_loader.get_image(image)
        self.image.set_colorkey(cfg.BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.orig_height = self.rect.h
        self.orig_width = self.rect.w
        self.hit_rect = self.rect

def collide_hit_rect(sprite_a, sprite_b):
    return sprite_a.hit_rect.colliderect(sprite_b.hit_rect)
