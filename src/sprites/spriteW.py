import pygame as pg

import src.config as cfg
import src.utility.sprite_loader as sprite_loader

class SpriteW(pg.sprite.Sprite):
    def __init__(self, x, y, image, groups):
        pg.sprite.Sprite.__init__(self, groups)
        self.image = sprite_loader.get_image(image)
        self.image.set_colorkey(cfg.BLACK)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        # self.rect might be transformed, so hit_rect will retain original dimensions.
        self.hit_rect = self.rect
        # Default id used in collision with bullets.
        self.id = -1

    def flip(self, xreflect, yreflect):
        old_center = self.rect.center
        self.image = pg.transform.flip(self.image, xreflect, yreflect)
        self.image.set_colorkey(cfg.BLACK)
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def rotate_image(self, rot):
        old_center = self.rect.center
        # Default image rotation means 0 rotation
        self.image = pg.transform.rotate(self.orig_image, rot)
        self.rect = self.image.get_rect()
        # Re-center the rectangle (assumes self.pos tracks center)
        self.rect.center = old_center

def collide_hit_rect(sprite_a, sprite_b):
    return sprite_a.hit_rect.colliderect(sprite_b.hit_rect)

def bullet_collide_id(sprite_a, sprite_b):
    # print(sprite_a.id != sprite_b.id)
    return sprite_a.hit_rect.colliderect(sprite_b.hit_rect) and \
            sprite_a.id != sprite_b.id
