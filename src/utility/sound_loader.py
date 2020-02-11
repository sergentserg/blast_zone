import os
import pygame as pg

# from src.settings import SND_DIR
import src.config as cfg

class SoundLoader:
    def __init__(self):
        self.music = {}
        self.sfx = {}
        # Load all sounds
        for file in os.listdir(cfg.SND_DIR):
            if file.endswith(".wav"):
                filename = os.path.join(cfg.SND_DIR, file)
                self._load_sound(filename)

    def _load_sound(self, filename):
        self.sfx[filename] = pg.mixer.Sound(filename)

    def get_sfx(self, filename):
        if not self.sfx[filename]:
            self._load_sound(filename)
        return self.sfx[filename]

_sound_loader = SoundLoader()
get_sfx = _sound_loder.get_sfx.
