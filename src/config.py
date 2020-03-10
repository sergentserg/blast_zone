import pygame as pg
from os import path

# src directory
GAME_DIR = path.dirname(__file__)
IMG_DIR = path.join(GAME_DIR, 'img')
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
BLUE = (0, 255, 0)
GREEN = (0, 0, 255)


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
