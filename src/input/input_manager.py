from os import path
import json
import pygame as pg

import src.input.input_state as input_state

class InputManager:
    """ Processes mouse and keyboard input, determines which actions are
        triggered based on a file with key bindings, and passes the information
        to the game object.

    """
    
    def __init__(self, game, filename='key_bindings.json'):
        self.game = game
        self.key_bindings = {}
        self.active_bindings = {}

        # Load key bindings.
        bindings_path = path.join(path.dirname(__file__), filename)
        with open(bindings_path, 'r') as f:
            self.key_bindings = json.load(f)

        # Convert keycodes to ASCII codes (pygame enums).
        for bindings in self.key_bindings.values():
            for binding in bindings:
                binding['keycode'] = ord(binding['keycode'])

    def handle_inputs(self):
        # Update key/mouse state.
        input_state.update()

        # Clear bindings from last frame.
        self.active_bindings.clear()

        # Store active key bindings.
        for action, bindings in self.key_bindings.items():
            # Each action may have multiple bindings, i.e move with 'w' or 'up arrow'.
            for binding in bindings:
                if input_state.get_keystate(binding['keycode']) == binding['state_type']:
                    # Append to list of bindings.
                    self.active_bindings[action] = self.active_bindings.get(action, []).append(binding)

        # Pass bindings to UI and to game state (and hence, the player).
        self.game.ui.handle_input(self.active_bindings, input_state.get_mousestate(0), *pg.mouse.get_pos())
        self.game.state.handle_input(self.active_bindings, input_state.get_mousestate(0), *pg.mouse.get_pos())
