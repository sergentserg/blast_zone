import pygame as pg

import src.config as cfg
from src.entities.ai_mob import AIMob


class TurretCtrl(AIMob):
    def __init__(self, turret, target):
        AIMob.__init__(self, target)
        self._sprite = turret
        self.set_state(AIAttackState)

    @property
    def turret(self):
        return self._sprite


class AIAttackState:
    def __init__(self, ai):
        self._ai = ai

    def update(self, dt):
        if self._ai.turret.get_ammo_count() > 0 and self._ai.is_target_in_range():
            dir = self._ai.angle_to_target()
            self._ai.turret.fire(dir)
        else:
            self._ai.turret.attempt_reload()
