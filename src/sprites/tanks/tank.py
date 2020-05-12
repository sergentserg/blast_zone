import pygame as pg

import src.config as cfg
from src.sprites.spriteW import SpriteW, collide_hit_rect
from src.sprites.behaviors.movable import MovableNonlinear
from src.sprites.behaviors.rotatable import Rotatable
from src.sprites.behaviors.damageable import Damageable

vec = pg.math.Vector2


class Tank(SpriteW, MovableNonlinear, Rotatable, Damageable):
    ACCELERATION = 768
    KNOCKBACK = 100

    _SPEED_CUTOFF = 100
    _TRACK_DELAY = 100
    def __init__(self, x, y, img_file, groups):
        self._layer = cfg.TANK_LAYER
        SpriteW.__init__(self, x, y, img_file,
                            (groups['all'], groups['tanks'], groups['damageable']))
        MovableNonlinear.__init__(self, x, y)
        Rotatable.__init__(self)
        Damageable.__init__(self, self.hit_rect)
        self.groups = groups
        self.barrels = []
        self.hit_rect.center = self.pos
        self._last_track = 0

    def update(self, dt):
        self.rotate(dt)
        self.move(self.groups['obstacles'], dt)
        can_spawn_track = cfg.time_since(self._last_track) > Tank._TRACK_DELAY
        if self.vel.length_squared() > Tank._SPEED_CUTOFF and can_spawn_track:
            self._spawn_tracks()

    def _spawn_tracks(self):
        Tracks(*self.pos, self.hit_rect.height, self.hit_rect.height,
                                                    self.rot, self.groups)
        self._last_track = pg.time.get_ticks()

    def rotate_barrel(self, dir):
        for barrel in self.barrels:
            barrel.rot = dir
            barrel.rotate()

    def has_ammo(self):
        return self.barrels[0].has_ammo()

    def fire(self):
        for barrel in self.barrels:
            barrel.fire()

    def reload(self):
        for barrel in self.barrels:
            barrel.reload()

    def kill(self):
        for barrel in self.barrels:
            barrel.kill()
        super().kill()


class Tracks(SpriteW):
    image = 'tracksSmall.png'
    IMG_ROT = -90
    def __init__(self, x, y, scale_h, scale_w, rot, groups):
        self._layer = cfg.TRACKS_LAYER
        SpriteW.__init__(self, x, y, Tracks.image, groups['all'])
        # Transform and recenter.
        old_center = self.rect.center
        self.image = pg.transform.rotate(self.image, rot - Tracks.IMG_ROT)
        self.image = pg.transform.scale(self.image, (scale_h, scale_w))
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.alpha = 255

    def update(self, dt):
        # Fade effect.
        if self.alpha > 0:
            self.alpha -= 2
            self.image.set_alpha(self.alpha)
        else:
            self.kill()
