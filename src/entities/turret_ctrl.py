import pygame as pg

import src.config as cfg
from src.sprites.barrels.special_barrel import Turret

vec = pg.math.Vector2


class TurretCtrl:
    DETECT_RADIUS = (cfg.SCREEN_WIDTH ** 2 + cfg.SCREEN_WIDTH ** 2) / 4
    def __init__(self, x, y, target, type, style, groups):
        self.turret = Turret(x, y, type, style, groups)
        # Assigned immediately after creation.
        self.target = target
        self.state = AILazyState(self)
        self.pos = vec(*self.turret.rect.center)

    def set_state(self, state):
        self.state = state

    def update(self, dt):
        if self.target.alive() and self.turret.alive():
            self.state.update(dt)

    def target_sep(self):
        return self.target.pos - self.pos

    def fire(self, separation):
        dir = separation.angle_to(vec(1, 0))
        self.turret.fire(dir)

    def draw_health(self, surface, camera):
        self.turret.draw_health(surface, camera)

    def alive(self):
        return self.turret.alive()


class AIAttackState:
    DURATION = 5000
    def __init__(self, ai):
        self.ai = ai
        self.enter_time = pg.time.get_ticks()

    def update(self, dt):
        if cfg.time_since(self.enter_time) > AIAttackState.DURATION:
            self.ai.set_state(AILazyState(self.ai))
        else:
            separation_vec = self.ai.target_sep()
            if separation_vec.length_squared() < self.ai.DETECT_RADIUS:
                self.ai.fire(separation_vec)
            else:
                self.ai.set_state(AILazyState(self.ai))


class AILazyState:
    DURATION = 3000
    def __init__(self, ai):
        self.ai = ai
        self.enter_time = pg.time.get_ticks()

    def update(self, dt):
        separation_vec = self.ai.target_sep()
        if separation_vec.length_squared() < self.ai.DETECT_RADIUS and \
            cfg.time_since(self.enter_time) > AILazyState.DURATION:
            self.ai.set_state(AIAttackState(self.ai))
