import pygame as pg

print("Initializing all Blast Zone submodules...")

__all__ = ['img', 'maps', 'snd', 'sprites', 'ui', 'input']

# Initialize pyagme for submodules to use
pg.init()
pg.mixer.init()

# Must set mode to prevent video error
pg.display.set_mode()
