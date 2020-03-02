import pygame as pg
vec = pg.math.Vector2

import src.config as cfg
from src.sprites.spriteW import SpriteW
from src.sprites.behaviors.movable import MovableNonlinear
from src.sprites.behaviors.rotatable import Rotatable

class Tank(SpriteW, MovableNonlinear, Rotatable):
    ACCELERATION = 768
    ROT_SPEED = 75
    SPEED_CUTOFF = 100
    TRACK_DELAY = 100
    def __init__(self, x, y, img_file, groups):
        self._layer = cfg.TANK_LAYER
        SpriteW.__init__(self, x, y, img_file, groups)
        MovableNonlinear.__init__(self, x, y)
        Rotatable.__init__(self)
        self.groups = groups
        self.barrel = None
        self.barrel_offset = int(self.orig_height/3)
        self.last_track = 0
        # self.vel = (45, 55)
        # self.rot_speed = 60

    def set_barrel(self, barrel):
        pass

    def rotate_barrel(self, aim_vec):
        pointing = aim_vec - vec(*self.rect.center)
        dir = pointing.angle_to(vec(1, 0))
        self.barrel.rect.center = vec(*self.rect.center) + vec(self.barrel_offset, 0).rotate(-dir)
        self.barrel.rot = dir
        self.barrel.rotate()

    def fire(self):
        self.barrel.fire()

    def update(self, dt):
        # Call move? Should move check for collisions/out of bounds?
        self.rotate(dt)
        self.move(dt)
        if self.vel.length_squared() > self.SPEED_CUTOFF and (
                    pg.time.get_ticks() - self.last_track) > Tank.TRACK_DELAY:
            track_pos = self.pos
            Tracks(*track_pos, self.orig_height, self.orig_width, self.rot, self.groups)
            self.last_track = pg.time.get_ticks()

    # Override rotate to call barrel's rotate? Maybe, maybe not
    def rotate(self, dt):
        self.barrel.rotate(dt)
        super().rotate(dt)

    def __spawn_tracks(self):
        pass

    # Override kill to call barrel's kill?
    def kill(self):
        self.barrel.kill()
        super().kill()


class Tracks(SpriteW):
    image = 'tracksSmall.png'
    IMG_ROT = -90
    def __init__(self, x, y, scale_h, scale_w, rot, groups):
        self._layer = cfg.TRACKS_LAYER
        SpriteW.__init__(self, x, y, Tracks.image, groups)
        old_center = self.rect.center
        self.image = pg.transform.rotate(self.image, rot - Tracks.IMG_ROT)
        self.image = pg.transform.scale(self.image, (scale_h, scale_w))
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.alpha = 255

    def update(self, dt):
        if self.alpha > 0:
            self.alpha -= 2
            self.image.set_alpha(self.alpha)
        else:
            self.kill()
