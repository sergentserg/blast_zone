from os import path
import pygame as pg
vec = pg.math.Vector2

from src.sprites.spriteW import SpriteW
from src.sprites.behaviors.movable import Movable
from src.sprites.behaviors.rotatable import Rotatable
from src.utility.stats_loader import load_stats_data
import src.config as cfg

class Bullet(SpriteW, Movable):
    __bullet_stats = load_stats_data(path.join(path.dirname(__file__), 'bullet_stats.json'))

    TYPE = {"standard": 1, "power": 2, "rapid": 3}
    IMAGE_ROT = 90
    def __init__(self, x, y, dir, bullet_type, color, groups):
        img_file = "bullet{0}{1}.png".format(color, Bullet.TYPE.get(bullet_type))
        SpriteW.__init__(self, x, y, img_file, (groups['all'], groups['bullets']))
        Movable.__init__(self, x, y)
        self.__init_bullet(dir, bullet_type)
        self.walls_grp = groups['obstacles']

    def __init_bullet(self, dir, bullet_type):
        self._layer = cfg.ITEM_LAYER
        # Bullets images are rotated 90 deg by default
        Rotatable.rotate_image(self, self.image, dir - Bullet.IMAGE_ROT)
        self.stats = Bullet.__bullet_stats[bullet_type]
        self.vel = vec(self.stats["speed"], 0).rotate(-dir)
        self.spawn_time = pg.time.get_ticks()

    def update(self, dt):
        if (pg.time.get_ticks() - self.spawn_time) > self.stats["lifetime"]:
            self.kill()
        else:
            self.move(self.walls_grp, dt)
            # pass
