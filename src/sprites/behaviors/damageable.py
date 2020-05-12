import pygame as pg

import src.config as cfg

class Damageable:
    MAX_HEALTH = 100
    def __init__(self, hit_rect):
        self.health = self.MAX_HEALTH
        self.hit_rect = hit_rect
        self.bar_width = self.hit_rect.width
        self.bar_height = self.hit_rect.height // 3

    def heal(self, pct):
        self.health += self.MAX_HEALTH * pct
        if self.health > self.MAX_HEALTH:
            self.health = self.MAX_HEALTH

    def draw_health(self, surface, camera):
        # surface is generally the screen we draw on.
        pct = self.health / self.MAX_HEALTH
        color = cfg.WHITE
        if pct > 0.7:
            color = cfg.GREEN
        elif pct > 0.3:
            color = cfg.YELLOW
        elif pct >= 0:
            color = cfg.RED


        fill_rect = pg.Rect(self.hit_rect.x, self.hit_rect.y,
                                    self.bar_width * pct, self.bar_height)
        outline_rect = pg.Rect(self.hit_rect.x, self.hit_rect.y,
                                            self.bar_width, self.bar_height)

        pg.draw.rect(surface, color, camera.apply(fill_rect))
        pg.draw.rect(surface, cfg.WHITE, camera.apply(outline_rect), 2)
