import pygame as pg
vec = pg.math.Vector2

from src.input.input_state import InputState

class PlayerCtrl:
    # def __init__(self, tank)
    def __init__(self):
        # Load bindings from json file
        self.actions = {"fire": self.fire,
                        "forward": self.forward,
                        "reverse": self.reverse,
                        "ccw_turn": self.ccw_turn,
                        "cw_turn": self.cw_turn}

    def handle_keys(self, active_bindings):
        # Reset acceleration if no press
        self.tank.rot_speed = 0
        self.tank.acc = vec(0, 0)
        for name in active_bindings:
            # i.e. self.actions["fire"]
            if self.actions.get(name, None):
                self.actions[name]()

    def handle_mouse(self, mouse_state, mouse_x, mouse_y):
        aim_vec = vec(*pg.mouse.get_pos())
        self.tank.rotate_barrel(aim_vec)

        if mouse_state == InputState.JUST_PRESSED:
            self.fire()

    def fire(self):
        self.tank.fire()

    def forward(self):
        self.tank.acc = vec(self.tank.ACCELERATION, 0).rotate(-self.tank.rot)

    def reverse(self):
        self.tank.acc = vec(-self.tank.ACCELERATION, 0).rotate(-self.tank.rot)

    def ccw_turn(self):
        self.tank.rot_speed = self.tank.ROT_SPEED

    def cw_turn(self):
        self.tank.rot_speed = -self.tank.ROT_SPEED

    def set_tank(self, tank):
        self.tank = tank