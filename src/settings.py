import pygame as pg
from os import path

# Source directory
GAME_DIR = path.dirname(__file__)

# Screen Settings
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 800
TITLE = "Blast Zone"
FPS = 60


# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)

"Game fonts"
FONT_NAMES = ['arial', 'calibri']

#Sprite Layers (smallest is topmost)
EFFECTS_LAYER = 1
BARREL_LAYER = 2
BULLET_LAYER = 3
TANK_LAYER = 4
