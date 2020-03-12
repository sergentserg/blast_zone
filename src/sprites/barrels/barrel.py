import json
from os import path
import pygame as pg

import src.config as cfg
from src.sprites.spriteW import SpriteW
import src.utility.sound_loader as sfx_loader
from src.sprites.behaviors.rotatable import Rotatable
from src.sprites.bullets.bullet import Bullet
from src.utility.stats_loader import load_stats_data

vec = pg.math.Vector2

class Barrel(SpriteW, Rotatable):
    __barrel_stats = load_stats_data(path.join(path.dirname(__file__), 'barrel_stats.json'))
    TYPES = {"standard": 1, "power": 2, "rapid": 3}
    FIRE_SFX = 'shoot.wav'
    def __init__(self, x, y, type, image, groups, offset = 0):
        self._layer = cfg.BARREL_LAYER
        SpriteW.__init__(self, x, y, image, (groups['all'],))
        Rotatable.__init__(self)
        self.groups = groups
        # May group these in a json file for barrels too
        self.type = type
        # Default color
        self.color = 'Dark'
        self.ammo_count = Barrel.__barrel_stats[type]["max_ammo"]
        self._last_shot = 0
        self._fire_sfx = sfx_loader.get_sfx(Barrel.FIRE_SFX)
        # self.no_ammo_sfx = None

    def update(self, dt):
        pass

    def fire(self):
        if (pg.time.get_ticks() - self._last_shot) > Barrel.__barrel_stats[self.type]["fire_delay"]:
            if self.ammo_count > 0:
                self._spawn_bullet()
                self._fire_sfx.play()
            else:
                # self.no_ammo_sfx.play()
                pass

    def _spawn_bullet(self):
        fire_pos = vec(*self.rect.center) + \
                            vec(self.hit_rect.height, 0).rotate(-self.rot)
        Bullet(*fire_pos, self.rot, self.type, self.color, self.id, self.groups)
        MuzzleFlash(*fire_pos, self.rot, self.groups)
        self.ammo_count -= 1
        self._last_shot = pg.time.get_ticks()

    def reload_ammo(self):
        self.ammo_count = Barrel.__barrel_stats[self.type]["max_ammo"]

    # Override: remove circular reference to parent tank before killing.
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
        if (pg.time.get_ticks() - self._spawn_time) > MuzzleFlash.FLASH_DURATION:
            self.kill()
