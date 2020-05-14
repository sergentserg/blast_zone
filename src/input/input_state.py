import pygame as pg

class InputState:
    STILL_RELEASED, JUST_PRESSED, STILL_PRESSED, JUST_RELEASED = 0, 1, 2, 3
    def __init__(self):
        # Keyboard state boolean list.
        self._current_keys = pg.key.get_pressed()
        self._prev_keys = None

        # Mouse state boolean list.
        self.current_mouse = pg.mouse.get_pressed()
        self.prev_mouse = None

    def update(self):
        self._prev_keys = self._current_keys
        self._current_keys = pg.key.get_pressed()

        self.prev_mouse = self.current_mouse
        self.current_mouse = pg.mouse.get_pressed()

    @classmethod
    def _get_state(self, prev, current, keycode):
        if prev[keycode]:
            if current[keycode]:
                return InputState.STILL_PRESSED
            else:
                return InputState.JUST_RELEASED
        else:
            if current[keycode]:
                return InputState.JUST_PRESSED
            else:
                return InputState.STILL_RELEASED

    def get_keystate(self, keycode):
        return self._get_state(self._prev_keys, self._current_keys, keycode)

    def get_mousestate(self, button):
        return self._get_state(self.prev_mouse, self.current_mouse, button)

_input_state = InputState()
get_keystate = _input_state.get_keystate
get_mousestate = _input_state.get_mousestate
update = _input_state.update
