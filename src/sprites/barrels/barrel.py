import json
from os import path
import pygame as pg
from ..spriteW import SpriteW
vec = pg.math.Vector2
from src.sprites.interfaces.rotatable import Rotatable
from src.sprites.bullets.bullet import Bullet
from src.utility.stats_loader import load_stats_data
from src.settings import BARREL_LAYER

class Barrel(SpriteW, Rotatable):
    __barrel_stats = load_stats_data(path.join(path.dirname(__file__), 'barrel_stats.json'))
    # TYPE = {"standard": 2, "power": 1, "rapid": 2}
    def __init__(self, x, y, type, img_file, groups, offset = 0):
        self._layer = BARREL_LAYER
        self.groups = groups
        SpriteW.__init__(self, x, y, img_file, groups)
        Rotatable.__init__(self)
        self.rect.midtop = (x, y)
        # May groupd these in a json file for barrels too
        self.type = type
        self.ammo_count = Barrel.__barrel_stats[type]["max_ammo"]
        self.last_shot = pg.time.get_ticks()
        # Sound effects for firing/failing to fire
        # self.fire_sfx = None
        # self.no_ammo_sfx = None

    def update(self, dt):
        pass

    def fire(self):
        if (pg.time.get_ticks() - self.last_shot) > Barrel.__barrel_stats[self.type]["fire_delay"]:
            if self.ammo_count > 0:
                self.__spawn_bullet()
                # self.fire_sfx.play()
            else:
                # self.no_ammo_sfx.play()
                pass

    def __spawn_bullet(self):
        # spawn bullet at barrel's nose
        bullet_pos = vec(*self.rect.center) #+ vec(int(self.rect.h), 0).rotate(-self.rot)
        Bullet(bullet_pos.x, bullet_pos.y, self.rot, self.type, self.color, self.groups)
        self.ammo_count -= 1
        self.last_shot = pg.time.get_ticks()

    def reload_ammo(self):
        self.ammo_count = Barrel.__barrel_stats[self.type]["max_ammo"]

    # overload
    def kill(self):
        # Call parent .kill()
        # super().kill()
        pass
