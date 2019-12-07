from .input_state import InputState
import json

class InputManager:
    def __init__(self):
        # Load key bindings
        self.key_bindings = {}
        self.active_bindings = {}

    # Need to allow for multiple keys
    def add_binding(self, name, keycode, state_type):
        # If key doesnt exist, set it, otherwise append
        self.key_bindings[name].append("keycode": keycode, "state_type": state_type})

    def init_bindings(self):
        with open('key_bindings.json', r) as f:
            self.key_bindings = json.load(f)


    def update(self, dt):
        pass
