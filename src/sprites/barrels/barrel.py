import json
from os import path
import pygame as pg

from ..spriteW import SpriteW
vec = pg.math.Vector2
from src.sprites.interfaces.rotatable import Rotatable
from src.sprites.bullets.bullet import Bullet
from src.utility.stats_loader import load_stats_data
from src.settings import BARREL_LAYER, EFFECTS_LAYER

class Barrel(SpriteW, Rotatable):
    __barrel_stats = load_stats_data(path.join(path.dirname(__file__), 'barrel_stats.json'))
    TYPES = {"standard": 1, "power": 2, "rapid": 3}
    def __init__(self, x, y, type, image, groups, offset = 0):
        self._layer = BARREL_LAYER
        SpriteW.__init__(self, x, y, image, groups)
        Rotatable.__init__(self)
        # Get rid of this at some point...
        self.offset = offset
        self.groups = groups
        self.rect.midtop = (x, y)
        # May group these in a json file for barrels too
        self.type = type
        self.ammo_count = Barrel.__barrel_stats[type]["max_ammo"]
        self.last_shot = 0
        # Sound effects for firing/failing to fire
        # self.fire_sfx = None
        # self.no_ammo_sfx = None

    def update(self, dt):
        pass

    def fire(self):
        if (pg.time.get_ticks() - self.last_shot) > Barrel.__barrel_stats[self.type]["fire_delay"]:
            if self.ammo_count > 0:
                self.__spawn_bullet()
                #
                # self.fire_sfx.play()
            else:
                # self.no_ammo_sfx.play()
                pass

    def __spawn_bullet(self):
        fire_pos = vec(*self.rect.center) + vec(self.orig_height, 0).rotate(-self.rot)
        Bullet(*fire_pos, self.rot, self.type, self.color, self.groups)
        MuzzleFlash(*fire_pos, self.rot, self.groups)
        self.ammo_count -= 1
        self.last_shot = pg.time.get_ticks()

    def reload_ammo(self):
        self.ammo_count = Barrel.__barrel_stats[self.type]["max_ammo"]

    # overload
    def kill(self):
        self.parent = None
        super().kill()

class MuzzleFlash(SpriteW):
    IMG_ROT = -90
    FLASH_DURATION = 25
    image = 'shotLarge.png'
    def __init__(self, x, y, rot, groups):
        self._layer = EFFECTS_LAYER
        SpriteW.__init__(self, x, y, MuzzleFlash.image, groups)
        Rotatable.rotate_image(self, self.image, rot - MuzzleFlash.IMG_ROT)
        self.spawn_time = pg.time.get_ticks()

    def update(self, dt):
        pass
        if (pg.time.get_ticks() - self.spawn_time) > MuzzleFlash.FLASH_DURATION:
            self.kill()
