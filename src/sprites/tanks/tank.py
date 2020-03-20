import pygame as pg

import src.config as cfg
from src.sprites.spriteW import SpriteW, collide_hit_rect
from src.sprites.behaviors.movable import MovableNonlinear
from src.sprites.behaviors.rotatable import Rotatable

vec = pg.math.Vector2

class Tank(SpriteW, MovableNonlinear, Rotatable):
    ACCELERATION = 768
    ROT_SPEED = 75
    MAX_HEALTH = 100

    _SPEED_CUTOFF = 100
    _TRACK_DELAY = 100
    def __init__(self, x, y, img_file, groups):
        self._layer = cfg.TANK_LAYER
        SpriteW.__init__(self, x, y, img_file, (groups['all'], groups['tanks']))
        MovableNonlinear.__init__(self, x, y)
        Rotatable.__init__(self)
        self.groups = groups
        self.barrels = []
        self.health = Tank.MAX_HEALTH
        self.hit_rect.center = self.pos
        # Time last track was spawned.
        self._last_track = 0

    def update(self, dt):
        # Call move? Should move check for collisions/out of bounds?
        self.rotate(dt)
        self.move(self.groups['obstacles'], dt)
        if self.vel.length_squared() > Tank._SPEED_CUTOFF and (
                    pg.time.get_ticks() - self._last_track) > Tank._TRACK_DELAY:
            self._spawn_tracks()

    def _handle_walls(self, displacement, walls_grp):
        # Collision in x direction.
        self.pos.x += displacement.x
        self.hit_rect.centerx = self.pos.x
        wall = pg.sprite.spritecollideany(self, walls_grp, collide_hit_rect)

        if wall:
            # self.pos.x -= displacement.x
            if self.pos.x < wall.rect.centerx:
                self.pos.x = wall.rect.left - self.hit_rect.width / 2
            else:
                self.pos.x = wall.rect.right + self.hit_rect.width / 2
            self.vel.x = 0
            self.hit_rect.centerx = self.pos.x

        # Collision in y direction.
        self.pos.y += displacement.y
        self.hit_rect.centery = self.pos.y
        wall = pg.sprite.spritecollideany(self, walls_grp, collide_hit_rect)

        if wall:
            self.pos.y -= self.vel.y
            # Hit top of wall.
            if self.pos.y < wall.rect.centery:
                self.pos.y = wall.rect.top - self.hit_rect.height / 2
            # Hit bottom of wall.
            else:
                self.pos.y = wall.rect.bottom + self.hit_rect.height / 2
            self.vel.y = 0
            self.hit_rect.centery = self.pos.y
        self.rect.center = self.pos

    def rotate_barrel(self, dir):
        # dir is a real number corresponding to the angle the barrel will face.
        for barrel in self.barrels:
            barrel.rot = dir
            barrel.rotate()

    def fire(self):
        for barrel in self.barrels:
            barrel.fire()

    def reload(self):
        for barrel in self.barrels:
            barrel.reload_ammo()

    # Override kill to call barrel's kill?
    def kill(self):
        for barrel in self.barrels:
            barrel.kill()
        super().kill()

    def draw_health(self, surface, camera):
        pct = self.health / Tank.MAX_HEALTH
        color = cfg.WHITE
        if pct > 0.7:
            color = cfg.GREEN
        elif pct > 0.3:
            color = cfg.YELLOW
        elif pct >= 0:
            color = cfg.RED

        bar_width = self.hit_rect.width
        bar_height = self.hit_rect.height // 3

        fill_rect = pg.Rect(self.hit_rect.x, self.hit_rect.y,
                                    bar_width * pct, bar_height)
        outline_rect = pg.Rect(self.hit_rect.x, self.hit_rect.y,
                                            bar_width, bar_height)

        pg.draw.rect(surface, color, camera.apply(fill_rect))
        pg.draw.rect(surface, cfg.WHITE, camera.apply(outline_rect), 2)

    def _spawn_tracks(self):
        Tracks(*self.pos, self.hit_rect.height, self.hit_rect.height,
                                                    self.rot, self.groups)
        self._last_track = pg.time.get_ticks()


class Tracks(SpriteW):
    image = 'tracksSmall.png'
    IMG_ROT = -90
    def __init__(self, x, y, scale_h, scale_w, rot, groups):
        self._layer = cfg.TRACKS_LAYER
        SpriteW.__init__(self, x, y, Tracks.image, groups['all'])
        # Transform and recenter.
        old_center = self.rect.center
        self.image = pg.transform.rotate(self.image, rot - Tracks.IMG_ROT)
        self.image = pg.transform.scale(self.image, (scale_h, scale_w))
        self.rect = self.image.get_rect()
        self.rect.center = old_center
        self.alpha = 255

    def update(self, dt):
        # Fade effect.
        if self.alpha > 0:
            self.alpha -= 2
            self.image.set_alpha(self.alpha)
        else:
            self.kill()
