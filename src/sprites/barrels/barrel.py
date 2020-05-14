import math
from os import path
import pygame as pg

import src.config as cfg
import src.utility.sound_loader as sfx_loader
from src.utility.stats_loader import load_stats_data
from src.sprites.spriteW import SpriteW
from src.sprites.behaviors.rotatable import Rotatable
from src.sprites.bullets.bullet import Bullet

vec = pg.math.Vector2


class Barrel(SpriteW, Rotatable):
    _STATS = load_stats_data(path.join(path.dirname(__file__), 'barrel_stats.json'))
    TYPES = {"standard": 1, "power": 2, "rapid": 3}
    FIRE_SFX = 'shoot.wav'
    RELOAD_TIMER = 10000
    def __init__(self, parent, offset, image, groups, type="standard"):
        self._layer = cfg.BARREL_LAYER
        SpriteW.__init__(self, *parent.rect.center, image, (groups['all'],))
        Rotatable.__init__(self)
        self.groups = groups

        # Parameters used for position.
        self.parent = parent
        self.offset = offset

        # Bullet parameters.
        self.type = type
        self.color = 'Dark'
        self.ammo_count = Barrel._STATS[self.type]["max_ammo"]

        self._last_shot = -math.inf
        self._fire_sfx = sfx_loader.get_sfx(Barrel.FIRE_SFX)
        # self.no_ammo_sfx = None

    def update(self, dt):
        self.rect.center = vec(*self.parent.rect.center) + \
                                    vec(self.offset, 0).rotate(-self.rot)

    def fire(self):
        if cfg.time_since(self._last_shot) > Barrel._STATS[self.type]["fire_delay"]:
            if self.has_ammo():
                self._last_shot = pg.time.get_ticks()
                self._spawn_bullet()
                self._fire_sfx.play()
            else:
                if cfg.time_since(self._last_shot) > Barrel.RELOAD_TIMER:
                    self.reload()
                    print("reload!")
                else:
                    # self.no_ammo_sfx.play()
                    pass

    def _spawn_bullet(self):
        fire_pos = vec(*self.rect.center) + \
                            vec(self.hit_rect.height, 0).rotate(-self.rot)
        Bullet(*fire_pos, self.rot, self.type, self.color, self.id, self.groups)
        MuzzleFlash(*fire_pos, self.rot, self.groups)
        self.ammo_count -= 1

    def has_ammo(self):
        return self.ammo_count > 0

    def get_ammo_count(self):
        return self.ammo_count

    def reload(self):
        self.ammo_count = Barrel._STATS[self.type]["max_ammo"]

    # @Override, remove circular reference?
    def kill(self):
        self.parent = None
        super().kill()


class MuzzleFlash(SpriteW):
    IMG_ROT = -90
    FLASH_DURATION = 25
    image = 'shotLarge.png'
    def __init__(self, x, y, rot, groups):
        self._layer = cfg.EFFECTS_LAYER
        SpriteW.__init__(self, x, y, MuzzleFlash.image, groups['all'])
        Rotatable.rotate_image(self, self.image, rot - MuzzleFlash.IMG_ROT)
        self._spawn_time = pg.time.get_ticks()

    def update(self, dt):
        if cfg.time_since(self._spawn_time) > MuzzleFlash.FLASH_DURATION:
            self.kill()
