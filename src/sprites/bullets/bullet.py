from os import path
import json
import pygame as pg
vec = pg.math.Vector2
from src.sprites.spriteW import SpriteW
from src.sprites.interfaces.movable import Movable

def load_bullet_data():
    bullet_stats_path = path.join(path.dirname(__file__), 'bullet_stats.json')
    with open(bullet_stats_path, 'r') as f:
        bullet_data = json.load(f)
        bullet_dict = {bullet["type"]: bullet["stats"] for bullet in bullet_data}
    return bullet_dict

class Bullet(SpriteW, Movable):
    __bullet_dict = load_bullet_data()

    def __init__(self, x, y, dir, type, img_file, groups):
        SpriteW.__init__(self, x, y, img_file, groups)
        Movable.__init__(self, x, y)
        self.stats = Bullet.__bullet_dict[type]
        self.vel = vec(0, -self.stats["speed"]).rotate(dir)
        print(self.vel)
        self.spawn_time = pg.time.get_ticks()

    def update(self, dt):
        if (pg.time.get_ticks() - self.spawn_time) > self.stats["lifetime"]:
            self.kill()
        else:
            self.move(dt)
