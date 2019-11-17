import pygame as pg
import json
from os import path

class InputKeys:
    STILL_RELEASED, JUST_PRESSED, JUST_RELEASED, STILL_PRESSED = 0, 1, 2, 3
    def __init__(self):
        self.current_state = pg.key.get_pressed()
        self.last_state = self.current_state

    def update_keys(self):
        self.last_state = self.current_state
        self.current_state = pg.key.get_pressed()

    def get_keystate(self, keycode):
        if self.last_state[keycode]:
            if self.current_state[keycode]:
                return InputKeys.STILL_PRESSED
            else:
                return InputKeys.JUST_RELEASED
        else:
            if self.current_state[keycode]:
                return InputKeys.JUST_PRESSED
            else:
                return InputKeys.STILL_RELEASED

class InputManager:
    def __init__(self):
        self.input_dir = path.dirname(__file__)
        self.input_keys = InputKeys()
        self.all_bindings = {}
        self.init_bindings()

    def update(self, dt):
        pass

    def add_binding(self, name = 1, code = 2, type = 3):
        """ addBinding(): adds a key binding to trigger an action with a key
            name: action name, e.g., 'fire',
            code: key code for action, e.g., pygame.K_a,
            type: key state, e.g., JustPressed, JustReleased

        """
        self.input_keys.update_keys()
        if self.input_keys.get_keystate(pg.K_a) == InputKeys.JUST_PRESSED:
            print("a was pressed")
            with open(path.join(self.input_dir, 'key_bindings.json'), 'r+') as f:
                all_bindings = json.load(f)
                if "a" not in all_bindings["fire"]:
                    all_bindings["fire"].append("a")
                f.seek(0)
                f.truncate()
                json.dump(all_bindings, f, indent = 4)

    def init_bindings(self):
        """ initBindings(): parses key bindings from a file """
        with open(path.join(self.input_dir, 'key_bindings.json'), 'r') as f:
            self.all_bindings = json.load(f)
        print(self.all_bindings)

input_handler = InputManager()
