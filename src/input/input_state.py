import pygame as pg

class InputState:
    STILL_RELEASED, JUST_PRESSED, STILL_PRESSED, JUST_RELEASED = 0, 1, 2, 3
    def __init__(self):
        # Keyboard
        self.current_keys = pg.key.get_pressed()
        self.prev_keys = None

        # Mouse
        self.current_mouse = pg.mouse.get_pressed()
        self.prev_mouse = None

    def update(self):
        self.prev_keys = self.current_keys
        self.current_keys = pg.key.get_pressed()

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
        return self._get_state(self.prev_keys, self.current_keys, keycode)

    def get_mousestate(self, button):
        return self._get_state(self.prev_mouse, self.current_mouse, button)

input_state = InputState()
