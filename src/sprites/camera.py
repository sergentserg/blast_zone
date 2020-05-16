import pygame as pg

import src.config as cfg

class Camera:
    def __init__(self, player, map_width, map_height):
        self._target = player.tank
        self.rect = pg.Rect(0, 0, cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT)
        self.rect.center = player.tank.pos
        self.map_width = map_width
        self.map_height = map_height

    def update(self):
        self.rect.center = self._target.pos

        if self._target.pos.x < cfg.SCREEN_WIDTH / 2:
            self.rect.x = 0
        elif self._target.pos.x > (self.map_width - cfg.SCREEN_WIDTH / 2):
            self.rect.x = self.map_width - cfg.SCREEN_WIDTH

        if self._target.pos.y < cfg.SCREEN_HEIGHT / 2:
            self.rect.y = 0
        elif self._target.pos.y > (self.map_height - cfg.SCREEN_HEIGHT / 2):
            self.rect.y = self.map_height - cfg.SCREEN_HEIGHT

    def apply(self, rect):
        return rect.move(-self.rect.x, -self.rect.y)
