import pygame as pg
from .buttons import Button
import src.settings as cfg
import src.input.input_manager as input_manager

class Menu:
    def __init__(self, title):
        self.title = title
        self.buttons = []
        self.current_button = 0

    def add_button(self, x, y, images, action, text, size, color):
        button = Button(x, y, images, action, text, size, color)
        self.buttons.append(button)

    def handle_mouse(self, mouse_x, mouse_y, mouse_state, dt):
        for button in self.buttons:
            button.handle_mouse(mouse_x, mouse_y, mouse_state, dt)

    def draw(self, surface):
        for button in self.buttons:
            surface.blit(button.img, button.rect)
