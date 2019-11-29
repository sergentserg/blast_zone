import pygame as pg
vec = pg.math.Vector2

class Rotatable:
    """ Class for Sprite objects that may rotate. Referenced instance variables,
        such as self.image and self.rect, belong to Sprite objects.

    """
    def __init__(self, rot = 0, rot_speed = 0):
        self.rot = rot
        self.rot_speed = rot_speed
        self.orig_image = self.image

    def rotate(self, dt):
        self.rot = (self.rot + self.rot_speed *  dt) % 360
        old_center = self.rect.center
        self.image = pg.transform.rotate(self.orig_image, self.rot)
        self.rect = self.image.get_rect()
        # Re-center the rectangle (assumes self.pos tracks center)
        self.rect.center = old_center
