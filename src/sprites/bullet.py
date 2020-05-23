import pygame as pg

import src.config as cfg
from src.utility.timer import Timer
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
          "standard": {"damage": 8, "speed": 500, "lifetime": 750},
          "rapid": {"damage": 6, "speed": 600, "lifetime": 750},
          "power": {"damage": 10, "speed": 400, "lifetime": 750}
}


class Bullet(SpriteW, Movable):
    IMAGE_ROT = 90
    def __init__(self, x, y, dir, type, color, id, groups):
        self._layer = cfg.ITEM_LAYER
        SpriteW.__init__(self, x, y, _IMAGES[type][color], (groups['all'], groups['bullets']))
        Movable.__init__(self, x, y)
        self.rotate_image(dir - Bullet.IMAGE_ROT)
        # Rotatable.rotate_image(self, self.image, dir - Bullet.IMAGE_ROT)
        self.hit_rect = self.rect
        self._damage = _STATS[type]["damage"]
        self.vel = cfg.Vec2(_STATS[type]["speed"], 0).rotate(-dir)
        self._lifetime = _STATS[type]["lifetime"]
        self._spawn_timer = Timer()
        self.id = id

    @classmethod
    def range(self, type):
        return _STATS[type]["speed"] * (_STATS[type]["lifetime"] / 1000)

    @property
    def damage(self):
        return self._damage

    def update(self, dt):
        if self._spawn_timer.elapsed_time() > self._lifetime:
            self.kill()
        else:
            self.move(dt)
