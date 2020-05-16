import pygame as pg

import src.config as cfg
from src.sprites.spriteW import SpriteW
from src.sprites.attributes.movable import Movable
from src.sprites.attributes.rotatable import Rotatable


_IMAGES = {
        "standard": {color: f"bullet{color}1.png"
                        for color in ["Blue", "Dark", "Green", "Red", "Sand"]},
        "power": {color: f"bullet{color}2.png"
                        for color in ["Blue", "Dark", "Green", "Red", "Sand"]},
        "rapid": {color: f"bullet{color}3.png"
                        for color in ["Blue", "Dark", "Green", "Red", "Sand"]}
}
_STATS = {
          "standard": {"damage": 8, "speed": 500, "lifetime": 750, "max_ammo": 20},
          "rapid": {"damage": 8, "speed": 600, "lifetime": 750, "max_ammo": 20},
          "power": {"damage": 8, "speed": 400, "lifetime": 750, "max_ammo": 20}
}


class Bullet(SpriteW, Movable):
    IMAGE_ROT = 90
    def __init__(self, x, y, dir, type, color, id, groups):
        self._layer = cfg.ITEM_LAYER
        SpriteW.__init__(self, x, y, _IMAGES[type][color], (groups['all'], groups['bullets']))
        Movable.__init__(self, x, y)
        Rotatable.rotate_image(self, self.image, dir - Bullet.IMAGE_ROT)
        self.hit_rect = self.rect
        self._damage = _STATS[type]["damage"]
        self.vel = cfg.Vec2(_STATS[type]["speed"], 0).rotate(-dir)
        self._lifetime = _STATS[type]["lifetime"]
        self._spawn_time = pg.time.get_ticks()
        self.id = id

    @classmethod
    def range(self, type):
        return _STATS[type]["speed"] * (_STATS[type]["lifetime"] / 1000)

    @property
    def damage(self):
        return self._damage

    def update(self, dt):
        if cfg.time_since(self._spawn_time) > self._lifetime:
            self.kill()
        else:
            self.move(dt)
