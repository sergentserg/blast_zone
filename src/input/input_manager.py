import pygame as pg

# 0, 0 -- STILL_RELEASED
# 0, 1 -- JUST_PRESSED
# 1, 0 -- JUST_RELEASED
# 1, 1 -- STILL_PRESSED
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

    def get_state(self, prev, current, keycode):
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

    def key_state(self, keycode):
        return self.get_state(self.prev_keys, self.current_keys, keycode)

    def get_mousestate(self, button):
        return self.get_state(self.prev_mouse, self.current_mouse, button)

input_state = InputState()
