import math
import pygame as pg

import src.config as cfg
import src.utility.sound_loader as sfx_loader
from src.sprites.spriteW import SpriteW
from src.sprites.attributes.rotatable import Rotatable
from src.sprites.bullet import Bullet
from src.sprites.obstacles import Barricade
from src.sprites.attributes.damageable import Damageable

_STATS = {
          "standard": {"fire_delay": 500, "max_ammo": 20},
          "rapid": {"fire_delay": 400, "max_ammo":20 },
          "power": {"fire_delay": 600, "max_ammo":20}
}

_BARREL_IMAGES = {}
for color in {"Blue", "Dark", "Green", "Red", "Sand"}:
    _BARREL_IMAGES[color] = {}
    for type in {("standard", 1), ("power", 2), ("rapid", 3)}:
        _BARREL_IMAGES[color][type[0]] = f"tank{color}_barrel{type[1]}.png"

_RELOAD_TIMER = 10000


class Barrel(SpriteW, Rotatable):
    FIRE_SFX = 'shoot.wav'
    def __init__(self, color, type, parent, offset, image, groups):
        self._layer = cfg.BARREL_LAYER
        SpriteW.__init__(self, *parent.rect.center, image, (groups['all'],))
        Rotatable.__init__(self)
        self.groups = groups

        # Bullet parameters.
        self._type = type
        self._color = color
        self._ammo_count = _STATS[self._type]["max_ammo"]

        # Parameters used for position.
        self._parent = parent
        self._offset = offset

        self._last_shot = -math.inf
        self._fire_sfx = sfx_loader.get_sfx(Barrel.FIRE_SFX)

    def update(self, dt):
        self.rect.center = cfg.Vec2(*self._parent.rect.center) + \
                                    self._offset.rotate(-self.rot)
    @property
    def range(self):
        return Bullet.range(self._type)

    def fire(self):
        if cfg.time_since(self._last_shot) > _STATS[self._type]["fire_delay"]:
            self._last_shot = pg.time.get_ticks()
            self._spawn_bullet()
            self._fire_sfx.play()

    def _spawn_bullet(self):
        fire_pos = cfg.Vec2(*self.rect.center) + \
                            cfg.Vec2(self.hit_rect.height, 0).rotate(-self.rot)
        Bullet(*fire_pos, self.rot, self._type, self._color, self.id, self.groups)
        MuzzleFlash(*fire_pos, self.rot, self.groups)
        self._ammo_count -= 1

    def can_reload(self):
        return cfg.time_since(self._last_shot) > _RELOAD_TIMER

    def get_ammo_count(self):
        return self._ammo_count

    def reload(self):
        self._ammo_count = _STATS[self._type]["max_ammo"]

    def kill(self):
        self._parent = None
        super().kill()


class SpecialBarrel(Barrel):
    def __init__(self, parent, offset, type, style, groups):
        """ type  is "standard", "power", or "rapid" """
        img_file = f'specialBarrel{style}.png'
        Barrel.__init__(self, "Dark", type, parent, offset, img_file, groups)


class Turret(Barricade, Damageable):
    def __init__(self, x, y, type, style, groups):
        Barricade.__init__(self, x, y, groups)
        Damageable.__init__(self, self.hit_rect)
        groups['damageable'].add(self)
        self._barrel = SpecialBarrel(self, cfg.Vec2(0, 0), type, style, groups)
        self.pos = self.rect.center
        # Bullets spawned by turret won't hurt turret, but hurts other sprites.
        self.id = id(self)
        self._barrel.id = self.id

    def kill(self):
        self._barrel.kill()
        super().kill()

    @property
    def range(self):
        return self._barrel.range

    def get_ammo_count(self):
        return self._barrel.get_ammo_count()

    def attempt_reload(self):
        if self._barrel.can_reload():
            self._barrel.reload()

    def fire(self, dir):
        self._barrel.rot = dir
        self._barrel.rotate()
        self._barrel.fire()


class MuzzleFlash(SpriteW):
    IMG_ROT = -90
    FLASH_DURATION = 25
    IMAGE = 'shotLarge.png'
    def __init__(self, x, y, rot, groups):
        self._layer = cfg.EFFECTS_LAYER
        SpriteW.__init__(self, x, y, MuzzleFlash.IMAGE, groups['all'])
        self.rotate_image(rot - MuzzleFlash.IMG_ROT)
        # Rotatable.rotate_image(self, self.image, rot - MuzzleFlash.IMG_ROT)
        self._spawn_time = pg.time.get_ticks()

    def update(self, dt):
        if cfg.time_since(self._spawn_time) > MuzzleFlash.FLASH_DURATION:
            self.kill()
