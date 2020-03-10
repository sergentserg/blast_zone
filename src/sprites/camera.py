import pygame as pg

import src.config as cfg

class Camera:
    def __init__(self, player, map_width, map_height):
        self.target = player
        self.rect = pg.Rect(0, 0, cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
        self.rect.center = player.tank.pos
        self.map_width = map_width
        self.map_height = map_height

    def update(self):
        self.rect.center = self.target.tank.pos

        if self.target.tank.pos.x < cfg.SCREEN_WIDTH / 2:
            self.rect.x = 0
        elif self.target.tank.pos.x > (self.map_width - cfg.SCREEN_WIDTH / 2):
            self.rect.x = self.map_width - cfg.SCREEN_WIDTH

        if self.target.tank.pos.y < cfg.SCREEN_HEIGHT / 2:
            self.rect.y = 0
        elif self.target.tank.pos.y > (self.map_height - cfg.SCREEN_HEIGHT / 2):
            self.rect.y = self.map_height - cfg.SCREEN_HEIGHT

    def apply(self, rect):
        return rect.move(-self.rect.x, -self.rect.y)
