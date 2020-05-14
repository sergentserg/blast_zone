import pygame as pg
vec = pg.math.Vector2

# Import to access the keystate enums.
import src.config as cfg
from src.input.input_state import InputState
import src.utility.game_text as gtext
import src.utility.sprite_loader as sprite_loader

# Tank options and stats.
_ROT_SPEED = 75

# Health Rect.
_HP_X_OFFSET = 5
_HP_Y_OFFSET = 5
_HP_WIDTH = cfg.SCREEN_WIDTH / 4
_HP_HEIGHT = _HP_WIDTH // 8

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
        if self.tank.alive():
            self.tank.fire()

    def forward(self):
        self.tank.acc = vec(self.tank.ACCELERATION, 0).rotate(-self.tank.rot)

    def reverse(self):
        self.tank.acc = vec(-self.tank.ACCELERATION, 0).rotate(-self.tank.rot)

    def ccw_turn(self):
        self.tank.rot_speed = _ROT_SPEED

    def cw_turn(self):
        self.tank.rot_speed = -_ROT_SPEED

    def set_tank(self, tank):
        self.tank = tank

        # Ammo Icon
        self.ammo_surf = sprite_loader.get_image(f"bullet{tank.color}3_outline.png")
        self.ammo_rect = self.ammo_surf.get_rect()

        # Surface with HP amount.
        self.hp_surf = pg.Surface((_HP_HEIGHT * 4, self.ammo_rect.height))
        self.hp_rect = self.hp_surf.get_rect()

        # Ammo text surface
        self.ammo_count_surf = pg.Surface((_HP_HEIGHT * 2, self.ammo_rect.height))
        self.ammo_count_rect = self.ammo_count_surf.get_rect()

    def draw_hud(self, surface, camera):
        # Draw the health bar.
        hp_x, hp_y = camera.rect.x + _HP_X_OFFSET, camera.rect.y + _HP_Y_OFFSET
        bar_rect = pg.Rect(hp_x, hp_y, _HP_WIDTH, _HP_HEIGHT)
        self.tank.draw_health(surface, camera, bar_rect)

        # Draw the "HP" text.
        self.hp_rect.x = bar_rect.left
        self.hp_rect.y = bar_rect.bottom
        self.hp_surf.fill(cfg.BLACK)
        gtext.render(self.hp_surf, f"HP : {self.tank.health} / {self.tank.MAX_HEALTH}", 12, cfg.WHITE)
        surface.blit(self.hp_surf, camera.apply(self.hp_rect))

        # Draw ammo icon.
        self.ammo_rect.x = self.hp_rect.right
        self.ammo_rect.y = self.hp_rect.y
        surface.blit(self.ammo_surf, camera.apply(self.ammo_rect))

        # Ammo count
        self.ammo_count_rect.x = self.ammo_rect.right
        self.ammo_count_rect.y = self.ammo_rect.y
        self.ammo_count_surf.fill(cfg.BLACK)
        gtext.render(self.ammo_count_surf,
            f"{self.tank.get_ammo_count()} / {self.tank.max_ammo}",
            12, cfg.WHITE)

        surface.blit(self.ammo_count_surf, camera.apply(self.ammo_count_rect))
        # Draw ammo reload timer.
