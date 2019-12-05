from src.sprites.tanks.color_tank import ColorTank
import pygame as pg

class PlayerCtrl:
    def __init__(self):
        self.tank = ColorTank(x, y, color, groups)

    def handle_input(self, input_state, dt):
        aim_vec = pg.math.Vec2(*pg.mouse.get_pos())
        self.tank.rotate_barrel(aim_vec, dt)
