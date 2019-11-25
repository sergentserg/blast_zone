#Create a class for user inputs
import pygame as pg
from src.utility.game_text import text_renderer
from src.sprites.animated_sprite import AnimatedSprite
import src.input.input_manager as input_manager

class Button(AnimatedSprite):
    def __init__(self, x, y, action, text, filenames):
        AnimatedSprite.__init__(self, x, y, filenames)
        # self.anim_fps = 65
        for img in self.images:
            text_renderer.render(img, text['text'], text['size'], text['color'])
        self.action = action

    def handle_mouse(self, mouse_x, mouse_y, dt, mouse_state):
        # is mouse over button?
        if (self.rect.x <= mouse_x <= self.rect.x + self.rect.w) and (
                    self.rect.y <= mouse_y <= self.rect.y + self.rect.h):
            if (mouse_state == input_manager.InputState.JUST_PRESSED) or (
                mouse_state == input_manager.InputState.JUST_RELEASED):
                # self.action['execute']()
                self.anim_fps = 1/self.dt
                self.update_anim(dt)
                # self.frame_time = 0
                # if self.current_frame == self.past_frame:
                    # print("Stack, plz dont overflow\n\n\n")
