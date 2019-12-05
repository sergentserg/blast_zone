#Create a class for user inputs
import pygame as pg
from src.utility.game_text import text_renderer
from src.sprites.animated_sprite import AnimatedSprite
from src.input.input_manager import InputState

class Button(AnimatedSprite):
    HOVER_OFF, HOVER_ON, CLICKED = 0, 1, 2
    def __init__(self, x, y, img_files, action, **text):
        frame_info = [ {'start_frame': Button.HOVER_OFF, 'num_frames': 1},
                        {'start_frame': Button.HOVER_ON, 'num_frames': 1},
                        {'start_frame': Button.CLICKED, 'num_frames': 1}]
        AnimatedSprite.__init__(self, x, y, img_files, frame_info)
        # Add Text to buttons
        for img in self.images:
            text_renderer.render(img, **text)
        # on-click button function
        self.action = action

    def handle_mouse(self, mouse_x, mouse_y, mouse_state, dt):
        # Keep track of bottom of button
        old_bot = self.rect.bottomleft
        # check if mouse is hovering button
        if self.__is_hovering(mouse_x, mouse_y):
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

    def __is_hovering(self, mouse_x, mouse_y):
        if mouse_x < self.rect.left:
            return False
        if mouse_x > self.rect.right:
            return False
        if mouse_y < self.rect.top:
            return False
        if mouse_y > self.rect.bottom:
            return False
        return True
