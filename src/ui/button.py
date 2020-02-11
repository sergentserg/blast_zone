import pygame as pg
import src.utility.game_text as gtxt
from src.sprites.animated_sprite import AnimatedSprite
from src.input.input_state import InputState

class Button(AnimatedSprite):
    HOVER_OFF, HOVER_ON, CLICKED = 0, 1, 2
    def __init__(self, groups, img_files, action, **text):
        frame_info = [ {'start_frame': Button.HOVER_OFF, 'num_frames': 1},
                        {'start_frame': Button.HOVER_ON, 'num_frames': 1},
                        {'start_frame': Button.CLICKED, 'num_frames': 1}]
        AnimatedSprite.__init__(self, 0, 0, groups, img_files, frame_info)
        # Add Text to buttons
        for img in self.images:
            gtxt.render(img, **text)
        # on-click button function
        self.action = action

    def handle_mouse(self, mouse_state, mouse_x, mouse_y):
        # Keep track of bottom of button
        old_bot = self.rect.bottomleft
        # check if mouse is hovering button
        if self._is_hovering(mouse_x, mouse_y):
            self.change_anim(Button.HOVER_ON)
            if mouse_state == InputState.STILL_PRESSED:
                self.change_anim(Button.CLICKED)
            elif mouse_state == InputState.JUST_RELEASED:
                # toggle-off clicked animation
                self.action()
        else:
            self.change_anim(Button.HOVER_OFF)
        # Update button position
        self.rect = self.image.get_rect()
        self.rect.bottomleft = old_bot

    def _is_hovering(self, mouse_x, mouse_y):
        if mouse_x < self.rect.left:
            return False
        if mouse_x > self.rect.right:
            return False
        if mouse_y < self.rect.top:
            return False
        if mouse_y > self.rect.bottom:
            return False
        return True
