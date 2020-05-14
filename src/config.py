import pygame as pg
from os import path


def time_since(t0):
    return pg.time.get_ticks() - t0

# src directory
GAME_DIR = path.dirname(__file__)
IMG_DIR = path.join(GAME_DIR, 'img')
EXTRA_IMG_DIR = path.join(IMG_DIR, 'other_images')
MAP_DIR = path.join(GAME_DIR, 'maps')
SND_DIR = path.join(GAME_DIR, 'snd')

# Screen Settings
SCREEN_WIDTH = 840
SCREEN_HEIGHT = 680
TITLE = "Blast Zone"
FPS = 60

# Color RGBs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
TRANSPARENT = (255, 255, 255, 0)


# Spritesheets.
SPRITESHEET_DATA = (
    { "spritesheet": "onlyObjects_default.png","xml": "onlyObjects_default.xml"},
    {"spritesheet": "blueSheet.png","xml": "blueSheet.xml"})

# Game font names
FONT_NAMES = ['arial', 'calibri']

#Sprite Layers (smallest is topmost)
EFFECTS_LAYER = 5
BARREL_LAYER = 4
ITEM_LAYER = 3
TANK_LAYER = 2
TRACKS_LAYER = 1

# Other constants.
Vec2 = pg.math.Vector2
UNIT_VEC = Vec2(1, 0)
