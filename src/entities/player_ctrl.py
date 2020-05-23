import pygame as pg

# Import to access the keystate enums.
import src.config as cfg
from src.input.input_state import InputState
import src.utility.game_text as gtext
import src.utility.sprite_loader as sprite_loader
from src.utility.timer import Timer
from src.sprites.barrel import RELOAD_DURATION

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
        self._actions = {"fire": self.fire,
                        "forward": self.forward,
                        "reverse": self.reverse,
                        "ccw_turn": self.ccw_turn,
                        "cw_turn": self.cw_turn}
        # A camera and tank are assigned once the level is created.
        self.camera = None
        self._tank = None
        self._ammo_timer = None

    def handle_keys(self, active_bindings):
        # Reset acceleration if no press
        self._tank.rot_speed = 0
        self._tank.acc = cfg.Vec2(0, 0)
        for name in active_bindings:
            # i.e. self._actions["fire"]
            if self._actions.get(name, None):
                self._actions[name]()

    def handle_mouse(self, mouse_state, mouse_x, mouse_y):
        aim_vec = cfg.Vec2(mouse_x + self.camera.rect.x, mouse_y + self.camera.rect.y)
        pointing = aim_vec - self._tank.pos
        dir = pointing.angle_to(cfg.Vec2(1, 0))
        self._tank.rotate_barrel(dir)

        self._tank.attempt_reload()
        if mouse_state == InputState.JUST_PRESSED:
            self.fire()

    def fire(self):
        ammo = self._tank.get_ammo_count()
        if ammo > 0:
            if ammo == 1:
                self._ammo_timer = Timer()
            self._tank.fire()

    def forward(self):
        self._tank.acc = cfg.Vec2(self._tank.ACCELERATION, 0).rotate(-self._tank.rot)

    def reverse(self):
        self._tank.acc = cfg.Vec2(-self._tank.ACCELERATION, 0).rotate(-self._tank.rot)

    def ccw_turn(self):
        self._tank.rot_speed = _ROT_SPEED

    def cw_turn(self):
        self._tank.rot_speed = -_ROT_SPEED

    def alive(self):
        return self._tank.alive()

    @property
    def tank(self):
        return self._tank

    @tank.setter
    def tank(self, new_tank):
        self._tank = new_tank

        # Ammo Icon
        self.ammo_surf = sprite_loader.get_image(f"bullet{new_tank.color}3_outline.png")
        self.ammo_rect = self.ammo_surf.get_rect()

        # Ammo text surface
        self.ammo_count_surf = pg.Surface((_HP_HEIGHT * 2, self.ammo_rect.height))
        self.ammo_count_rect = self.ammo_count_surf.get_rect()

    def draw_hud(self, surface, camera):
        # Draw the health bar.
        hp_x, hp_y = camera.rect.x + _HP_X_OFFSET, camera.rect.y + _HP_Y_OFFSET
        bar_rect = pg.Rect(hp_x, hp_y, _HP_WIDTH, _HP_HEIGHT)
        self._tank.draw_health(surface, camera, bar_rect)

        hp_text_pos = camera.apply(bar_rect).center
        gtext.render_pos(surface, *hp_text_pos, f"HP: {self._tank.health} / {self._tank.MAX_HEALTH}", 16, cfg.WHITE)

        # Draw ammo icon.
        self.ammo_rect.x = bar_rect.left
        self.ammo_rect.y = bar_rect.bottom + 5
        surface.blit(self.ammo_surf, camera.apply(self.ammo_rect))

        # Ammo count
        self.ammo_count_rect.x = self.ammo_rect.right + 2
        self.ammo_count_rect.y = self.ammo_rect.y
        self.ammo_count_surf.fill(cfg.BLACK)

        if self._tank.get_ammo_count() == 0:
            ammo_text = f"{(RELOAD_DURATION - self._ammo_timer.elapsed_time()) // 1000}"
        else:
            ammo_text = f"{self._tank.get_ammo_count()} / {self._tank.max_ammo}"
        gtext.render(self.ammo_count_surf, ammo_text, 12, cfg.WHITE)
        surface.blit(self.ammo_count_surf, camera.apply(self.ammo_count_rect))
