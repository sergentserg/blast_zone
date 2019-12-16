import json
from os import path
import pygame as pg

from src.input.input_state import input_state

class InputManager:
    def __init__(self, game):
        # Load key bindings
        self.game = game
        self.key_bindings = {}
        self.active_bindings = {}
        self._load_bindings()

    def _load_bindings(self):
        bindings_path = path.join(path.dirname(__file__), 'key_bindings.json')
        with open(bindings_path, 'r') as f:
            self.key_bindings = json.load(f)

        # Convert to ASCII code (equivalent to pygame keyboard enums).
        for bindings in self.key_bindings.values():
            for bind_info in bindings:
                bind_info['keycode'] = ord(bind_info['keycode'])

    def handle_inputs(self):
        input_state.update()
        self.active_bindings.clear()

        # Store active key bindings
        for action, bindings in self.key_bindings.items():
            # Each action may have multiple bindings
            for bind_info in bindings:
                if input_state.get_keystate(bind_info['keycode']) == bind_info['state_type']:
                    self.active_bindings[action] = self.active_bindings.get(action, []).append(bind_info)

        # Pass bindings to UI and to player
        self.game.ui.handle_keys(self.active_bindings)
        self.game.state.handle_keys(self.active_bindings)

        self.game.ui.handle_mouse(input_state.get_mousestate(0), *pg.mouse.get_pos())
        self.game.state.handle_mouse(input_state.get_mousestate(0), *pg.mouse.get_pos())
