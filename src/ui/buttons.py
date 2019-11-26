#Create a class for user inputs
import pygame as pg
from src.utility.game_text import text_renderer
from src.sprites.animated_sprite import AnimatedSprite
from src.input.input_manager import InputState

class Button(AnimatedSprite):
    HOVER_OFF, HOVER_ON, CLICKED = 0, 1, 2
    def __init__(self, x, y, action, text, img_files):
        frame_info = [(Button.HOVER_OFF, 1), (Button.HOVER_ON, 1), (Button.CLICKED, 1)]
        AnimatedSprite.__init__(self, x, y, img_files, frame_info)
        # Add Text to buttons
        for img in self.images:
            text_renderer.render(img, text['text'], text['size'], text['color'])
        # on-click button function
        self.action = action

    def handle_mouse(self, mouse_x, mouse_y, mouse_state, dt):
        # Keep track of bottom of button
        old_bot = self.rect.bottomleft
        # check if mouse is hovering button
        if (self.rect.x <= mouse_x <= self.rect.x + self.rect.w) and (
                    self.rect.y <= mouse_y <= self.rect.y + self.rect.h):
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
