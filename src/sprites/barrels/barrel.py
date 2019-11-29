import json
import pygame as pg
from ..spriteW import SpriteW
vec = pg.math.Vector2
from src.sprites.interfaces.rotatable import Rotatable
from src.sprites.bullets.bullet import Bullet

class Barrel(SpriteW, Rotatable):
    def __init__(self, x, y, img_file, groups):
        self.groups = groups
        SpriteW.__init__(self, x, y, img_file, groups)
        Rotatable.__init__(self)
        # May groupd these in a json file for barrels too
        self.type = "standard"
        self.fire_delay = 1000
        self.ammo_count = 20
        # Sound effects for firing/failing to fire
        # self.fire_sfx = None
        # self.no_ammo_sfx = None
        self.last_shot = pg.time.get_ticks()

    def update(self, dt):
        self.fire()

    def fire(self):
        if (pg.time.get_ticks() - self.last_shot) > self.fire_delay:
            if self.ammo_count > 0:
                # Spawn at bullet nose
                print(self.rot)
                bullet_pos = vec(*self.rect.center) + vec(self.rect.h/2, 0).rotate(-self.rot)
                bullet_img = 'bulletBlue2.png'
                Bullet(bullet_pos.x, bullet_pos.y, self.rot, self.type, bullet_img, self.groups)
                # self.fire_sfx.play()
                self.ammo_count -= 1
                self.last_shot = pg.time.get_ticks()
            else:
                # self.no_ammo_sfx.play()
                pass

    def reload_ammo(self):
        self.ammo_count = 0

    # overload
    def kill(self):
        pass
