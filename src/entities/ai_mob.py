import src.config as cfg

class AIMob:
    def __init__(self, target):
        self._target = target
        self._state = None
        self._sprite = None
        self._ray_to_target = None

    @property
    def target(self):
        return self._target

    @property
    def state(self):
        return self._state

    def update(self, dt):
        self._ray_to_target = self._target.pos - self._sprite.pos
        self._state.update(dt)

    def alive(self):
        return self._sprite.alive()

    def draw_health(self, surface, camera):
        self._sprite.draw_health(surface, camera)

    def set_state(self, state):
        self._state = state(self)

    def is_target_in_range(self):
        return self._target.alive() and \
            self._ray_to_target.length_squared() < self._sprite.range ** 2

    def angle_to_target(self):
        return self._ray_to_target.angle_to(cfg.UNIT_VEC)
