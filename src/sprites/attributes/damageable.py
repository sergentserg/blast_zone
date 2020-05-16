import pygame as pg

import src.config as cfg

class Damageable:
    MAX_HEALTH = 100
    def __init__(self, hit_rect):
        self.health = self.MAX_HEALTH
        self.hit_rect = hit_rect

    def heal(self, amount):
        self.health += amount
        if self.health > self.MAX_HEALTH:
            self.health = self.MAX_HEALTH

    def damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def draw_health(self, surface, camera, outline_rect=None):
        # surface is generally the screen we draw on.
        pct = self.health / self.MAX_HEALTH
        color = cfg.TRANSPARENT
        if pct > 0.7:
            color = cfg.GREEN
        elif pct > 0.3:
            color = cfg.YELLOW
        elif pct > 0:
            color = cfg.RED

        if outline_rect:
            fill_rect = outline_rect.copy()
        else:
            fill_rect = self.hit_rect.copy()
            fill_rect.height = fill_rect.height // 3
            outline_rect = fill_rect.copy()

        fill_rect.width *= pct

        pg.draw.rect(surface, color, camera.apply(fill_rect))
        pg.draw.rect(surface, cfg.BLACK, camera.apply(outline_rect), 2)
