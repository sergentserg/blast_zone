import math
import random
import pygame as pg
from itertools import cycle

import src.config as cfg
from src.sprites.tanks.color_tank import ColorTank


class AITankCtrl:
    DETECT_RADIUS = (cfg.SCREEN_WIDTH ** 2 + cfg.SCREEN_WIDTH ** 2) / 8
    def __init__(self, x, y, target, path_data, color, groups):
        self.tank = ColorTank(x, y, color, groups)
        self._target = target
        self._path_points = cycle([cfg.Vec2(p.x, p.y) for p in path_data])
        self._ray_to_target = None
        self._state = AIPatrolState(self, self.tank.pos)

    def update(self, dt):
        if self._target.alive():
            self._ray_to_target = self._target.pos - self.tank.pos
        self._state.update(dt)

    def set_state(self, state):
        if state == AIPatrolState:
            self._state = AIPatrolState(self, self.tank.pos)
        else:
            self._state = state(self)

    def turn_towards(self, point=None):
        if point:
            turn_vec = point - self.tank.pos
        else:
            turn_vec = self._target.pos - self.tank.pos
        dir = turn_vec.angle_to(cfg.UNIT_VEC)
        self.rotate_to(dir)

    def rotate_to(self, dir):
        self.tank.rot = dir
        self.tank.rotate()
        self.tank.rotate_barrel(dir)

    def get_target_direction(self):
        return self._ray_to_target.angle_to(cfg.UNIT_VEC)

    def move(self, pct=1):
        self.tank.acc = cfg.Vec2(self.tank.ACCELERATION * pct, 0).rotate(-self.tank.rot)

    def fire(self):
        self.tank.fire()

    def has_ammo(self):
        return self.tank.has_ammo()

    def is_target_in_range(self):
        return self._target.alive() and \
            self._ray_to_target.length_squared() < self.DETECT_RADIUS

    def get_next_destination(self):
        return next(self._path_points)

    def collided_with_wall(self):
        return self.tank.collided_with_wall()

    def alive(self):
        return self.tank.alive()

    def draw_health(self, surface, camera):
        self.tank.draw_health(surface, camera)


class AITankState:
    WALL_AVOID_DURATION = 1000
    WALL_TURN_ANGLE = 15
    def __init__(self, ai):
        self._ai = ai
        self._crash_time = -math.inf

    def check_for_walls(self):
        if self._ai.collided_with_wall():
            self._crash_time = pg.time.get_ticks()
            self._ai.rotate_to(self._ai.tank.rot + AITankState.WALL_TURN_ANGLE)

    def is_avoiding_wall(self):
        return cfg.time_since(self._crash_time) < AITankState.WALL_AVOID_DURATION


class AIPatrolState(AITankState):
    EPSILON = 100
    def __init__(self, ai, tank_pos):
        AITankState.__init__(self, ai)
        self._destination = self._ai.get_next_destination()
        self._ai.turn_towards(self._destination)
        self._ai_pos = tank_pos

    def update(self, dt):
        self.check_for_walls()
        if not self.is_avoiding_wall():
            if self._ai.is_target_in_range():
                self._ai.set_state(AIPursueState)
            else:
                if self.arrived():
                    self._destination = self._ai.get_next_destination()
                self._ai.turn_towards(self._destination)
        self._ai.move(pct=0.5)

    def arrived(self):
        dist = (self._destination - self._ai_pos).length_squared()
        return dist < AIPatrolState.EPSILON


class AIPursueState(AITankState):
    def __init__(self, ai):
        AITankState.__init__(self, ai)
        self.pursue_start = pg.time.get_ticks()

    def update(self, dt):
        self.check_for_walls()
        if not self.is_avoiding_wall():
            if self._ai.has_ammo():
                if self._ai.is_target_in_range():
                    self._ai.turn_towards()
                    self._ai.fire()
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
            if self._ai.has_ammo():
                self._ai.set_state(AIPatrolState)
            else:
                dir = self._ai.get_target_direction() + AIFleeState.FLEE_ANGLE
                self._ai.rotate_to(dir)
                # It 'tries' to fire, ultimately trigger barrel reload.
                self._ai.fire()
        self._ai.move()
