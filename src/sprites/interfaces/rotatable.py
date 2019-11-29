import pygame as pg
vec = pg.math.Vector2

class Rotatable:
    """ Class for Sprite objects that may rotate. Referenced instance variables,
        such as self.image and self.rect, belong to Sprite objects.

    """
    IMAGE_ROT = -90
    def __init__(self, rot_speed = 0):
        # Default rotation is 90 degrees CW
        self.rot = self.IMAGE_ROT
        self.rot_speed = rot_speed
        self.orig_image = self.image

    def rotate(self, dt):
        self.rot = (self.rot + self.rot_speed *  dt) % 360
        old_center = self.rect.center
        # Default image rotation means 0 rotation
        self.image = pg.transform.rotate(self.orig_image, self.rot - self.IMAGE_ROT)
        self.rect = self.image.get_rect()
        # Re-center the rectangle (assumes self.pos tracks center)
        self.rect.center = old_center
