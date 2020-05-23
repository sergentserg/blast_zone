import math
import random
import pygame as pg
from itertools import cycle

import src.config as cfg
from src.utility.timer import Timer
from src.entities.ai_mob import AIMob


class AITankCtrl(AIMob):
    def __init__(self, tank, path_data, target):
        AIMob.__init__(self, target)
        self._sprite = tank
        self._path_points = cycle([cfg.Vec2(p.x, p.y) for p in path_data])
        self.set_state(AIPatrolState)

    @property
    def tank(self):
        return self._sprite

    def rotate_to(self, dir):
        self._sprite.rot = dir
        self._sprite.rotate()
        self._sprite.rotate_barrel(dir)

    def move(self, pct=1):
        self._sprite.acc = cfg.Vec2(self._sprite.ACCELERATION * pct, 0).rotate(-self._sprite.rot)

    def get_next_destination(self):
        return next(self._path_points)


class AITankState:
    WALL_AVOID_DURATION = 1000
    WALL_TURN_ANGLE = 15
    def __init__(self, ai):
        self._ai = ai
        self._crash_timer = Timer()

    def check_for_walls(self):
        if self._ai.tank.collided_with_wall():
            self._crash_timer.restart()
            self._ai.rotate_to(self._ai.tank.rot + AITankState.WALL_TURN_ANGLE)

    def is_avoiding_wall(self):
        return self._crash_timer.elapsed_time() < AITankState.WALL_AVOID_DURATION


class AIPatrolState(AITankState):
    EPSILON = 100
    def __init__(self, ai):
        AITankState.__init__(self, ai)
        self._destination = self._ai.get_next_destination()
        dir = (self._destination - self._ai.tank.pos).angle_to(cfg.UNIT_VEC)
        self._ai.rotate_to(dir)

    def update(self, dt):
        self.check_for_walls()
        if not self.is_avoiding_wall():
            if self._ai.is_target_in_range():
                self._ai.set_state(AIPursueState)
            else:
                if self.arrived():
                    self._destination = self._ai.get_next_destination()

                dir = (self._destination - self._ai.tank.pos).angle_to(cfg.UNIT_VEC)
                self._ai.rotate_to(dir)
        self._ai.move(pct=0.5)

    def arrived(self):
        dist = (self._destination - self._ai.tank.pos).length_squared()
        return dist < AIPatrolState.EPSILON


class AIPursueState(AITankState):
    def __init__(self, ai):
        AITankState.__init__(self, ai)
        self.pursue_start = pg.time.get_ticks()

    def update(self, dt):
        self.check_for_walls()
        if not self.is_avoiding_wall():
            if self._ai.tank.get_ammo_count() > 0:
                if self._ai.is_target_in_range():
                    dir = self._ai.angle_to_target()
                    self._ai.rotate_to(dir)
                    self._ai.tank.fire()
                else:
                    self._ai.set_state(AIPatrolState)
            else:
                self._ai.set_state(AIFleeState)
        self._ai.move()


class AIFleeState(AITankState):
    # 180 to go opposite to player, and 30 for slight turn.
    FLEE_ANGLE = 210
    def __init__(self, ai):
        AITankState.__init__(self, ai)

    def update(self, dt):
        self.check_for_walls()
        if not self.is_avoiding_wall():
            if self._ai.tank.get_ammo_count() > 0:
                self._ai.set_state(AIPatrolState)
            else:
                # Run away from target.
                dir = self._ai.angle_to_target() + AIFleeState.FLEE_ANGLE
                self._ai.rotate_to(dir)
                self._ai.tank.attempt_reload()
        self._ai.move()
