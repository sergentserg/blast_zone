import pygame as pg
import src.config as cfg

# the first 3 are defult; the last 1 is a bigger buffer than default,
# helps with sound lag
pg.mixer.pre_init(44100, -16, 1, 2048)
pg.init()
# Init video subsystems
pg.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
