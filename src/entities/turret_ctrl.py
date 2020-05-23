import pygame as pg

import src.config as cfg
from src.entities.ai_mob import AIMob
from src.entities.tank_ctrl import AIPursueState


class TurretCtrl(AIMob):
    def __init__(self, turret, target, ai_boss):
        AIMob.__init__(self, target)
        self._sprite = turret
        self._ai_boss = ai_boss
        self.set_state(AIAttackState)

    def is_tank_pursuing(self):
        return self._ai_boss.alive() and type(self._ai_boss.state) == AIPursueState

    @property
    def turret(self):
        return self._sprite


class AIAttackState:
    def __init__(self, ai):
        self._ai = ai

    def update(self, dt):
        if self._ai.is_target_in_range():
            if self._ai.turret.get_ammo_count() > 0:
                if not self._ai.is_tank_pursuing():
                    dir = self._ai.angle_to_target()
                    self._ai.turret.fire(dir)
            else:
                self._ai.turret.attempt_reload()
