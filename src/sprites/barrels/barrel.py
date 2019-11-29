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
        # Decides bullet type
        self.type = "standard"
        self.fire_delay = 1000
        self.ammo = 20
        # self.fire_sfx = None
        # self.no_ammo_sfx = None
        self.last_shot = pg.time.get_ticks()
        self.rot += 90

    def update(self, dt):
        self.rotate(dt)
        self.fire()

    def fire(self):
        if (pg.time.get_ticks() - self.last_shot) > self.fire_delay:
            if self.ammo > 0:
                # Spawn at bullet nose
                bullet_pos = vec(*self.rect.center) + vec(0, -self.rect.h/2).rotate(self.rot)
                bullet_img = 'bulletBlue2.png'
                Bullet(bullet_pos.x, bullet_pos.y, self.rot, self.type, bullet_img, self.groups)
                # self.fire_sfx.play()
                self.ammo -= 1
                self.last_shot = pg.time.get_ticks()
            else:
                # self.no_ammo_sfx.play()
                pass

    def reload_ammo(self):
        self.ammo = 0

    # overload
    def kill(self):
        pass
