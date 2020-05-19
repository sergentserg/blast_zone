import pygame as pg


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

    def rotate(self, dt = 0):
        self.rot = (self.rot + self.rot_speed *  dt) % 360
        self.rotate_image(self.rot - self.IMAGE_ROT)
        # self.rotate_image(self, self.orig_image, self.rot - self.IMAGE_ROT)

    # @classmethod
    # def rotate_image(cls, sprite, orig_image, rot):
    #     old_center = sprite.rect.center
    #     # Default image rotation means 0 rotation
    #     sprite.image = pg.transform.rotate(orig_image, rot)
    #     sprite.rect = sprite.image.get_rect()
    #     # Re-center the rectangle (assumes self.pos tracks center)
    #     sprite.rect.center = old_center
