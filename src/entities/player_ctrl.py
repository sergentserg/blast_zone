import pygame as pg
vec = pg.math.Vector2

# Import to access the keystate enums.
import src.config as cfg
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
        # A camera and tank are assigned once the level is created.
        self.camera = None
        self.tank = None

    def handle_keys(self, active_bindings):
        # Reset acceleration if no press
        self.tank.rot_speed = 0
        self.tank.acc = vec(0, 0)
        for name in active_bindings:
            # i.e. self.actions["fire"]
            if self.actions.get(name, None):
                self.actions[name]()

    def handle_mouse(self, mouse_state, mouse_x, mouse_y):
        aim_vec = vec(mouse_x + self.camera.rect.x, mouse_y + self.camera.rect.y)
        pointing = aim_vec - self.tank.pos
        dir = pointing.angle_to(vec(1, 0))
        self.tank.rotate_barrel(dir)

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
