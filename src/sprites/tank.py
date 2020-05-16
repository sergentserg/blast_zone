import pygame as pg

import src.config as cfg
from src.sprites.spriteW import SpriteW, collide_hit_rect
from src.sprites.attributes.movable import MovableNonlinear
from src.sprites.attributes.rotatable import Rotatable
from src.sprites.attributes.damageable import Damageable
from src.sprites.barrel import Barrel


class Tank(SpriteW, MovableNonlinear, Rotatable, Damageable):
    ACCELERATION = 768
    KNOCKBACK = 100

    _SPEED_CUTOFF = 100
    _TRACK_DELAY = 100
    def __init__(self, x, y, img, groups):
        self._layer = cfg.TANK_LAYER
        SpriteW.__init__(self, x, y, img,
                            (groups['all'], groups['tanks'], groups['damageable']))
        MovableNonlinear.__init__(self, x, y)
        Rotatable.__init__(self)
        Damageable.__init__(self, self.hit_rect)
        self.groups = groups
        self._barrels = []
        self.hit_rect.center = self.pos
        self._last_track = 0

    def update(self, dt):
        self.rotate(dt)
        self.move(self.groups['obstacles'], dt)
        can_spawn_track = cfg.time_since(self._last_track) > Tank._TRACK_DELAY
        if self.vel.length_squared() > Tank._SPEED_CUTOFF and can_spawn_track:
            self._spawn_tracks()

    @property
    def range(self):
        return self._barrels[0].range

    def _spawn_tracks(self):
        Tracks(*self.pos, self.hit_rect.height, self.hit_rect.height,
                                                    self.rot, self.groups)
        self._last_track = pg.time.get_ticks()

    def rotate_barrel(self, dir):
        for barrel in self._barrels:
            barrel.rot = dir
            barrel.rotate()

    def get_ammo_count(self):
        return self._barrels[0].get_ammo_count()

    def has_ammo(self):
        return self._barrels[0].has_ammo()

    def fire(self):
        for barrel in self._barrels:
            barrel.fire()

    def attempt_reload(self):
        if self._barrels[0].can_reload():
            self.reload()

    def reload(self):
        for barrel in self._barrels:
            barrel.reload()

    def kill(self):
        for barrel in self._barrels:
            barrel.kill()
        super().kill()


# Color barrel images.
_BARREL_IMAGES = {}
for color in {"Blue", "Dark", "Green", "Red", "Sand"}:
    _BARREL_IMAGES[color] = {}
    for type in {("standard", 1), ("power", 2), ("rapid", 3)}:
        _BARREL_IMAGES[color][type[0]] = f"tank{color}_barrel{type[1]}.png"

class ColorTank(Tank):
    def __init__(self, x, y, color, type, groups):
        img = f"tankBody_{color}_outline.png"
        Tank.__init__(self, x, y, img, groups)
        self.id = id(self)
        # Create, position, and assign id to barrel.
        offset = self.hit_rect.height // 3
        self.color = color.capitalize()
        barrel = Barrel(self.color, type, self, offset, _BARREL_IMAGES[self.color][type], groups)
        # barrel.rect.midtop = self.rect.center
        barrel.id = self.id
        self._barrels.append(barrel)
        self.max_ammo = self._barrels[0].get_ammo_count()


class Tracks(SpriteW):
    IMAGE = 'tracksSmall.png'
    IMG_ROT = -90
    def __init__(self, x, y, scale_h, scale_w, rot, groups):
        self._layer = cfg.TRACKS_LAYER
        SpriteW.__init__(self, x, y, Tracks.IMAGE, groups['all'])
        # Transform and recenter.
        old_center = self.rect.center
        self.image = pg.transform.rotate(self.image, rot - Tracks.IMG_ROT)
        self.image = pg.transform.scale(self.image, (scale_h, scale_w))
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self._alpha = 255

    def update(self, dt):
        # Fade effect.
        if self._alpha > 0:
            self._alpha -= 2
            self.image.set_alpha(self._alpha)
        else:
            self.kill()
