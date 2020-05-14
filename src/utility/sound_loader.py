import os
import pygame as pg

import src.config as cfg

class SoundLoader:
    def __init__(self):
        self._music = {}
        self._sfx = {}
        # Load all sounds
        for file in os.listdir(cfg.SND_DIR):
            if file.endswith(".wav"):
                filepath = os.path.join(cfg.SND_DIR, file)
                self._load_sound(filepath)

    def _load_sound(self, filepath):
        self._sfx[filepath] = pg.mixer.Sound(filepath)

    def get_sfx(self, filename):
        filepath = os.path.join(cfg.SND_DIR, filename)
        if not self._sfx[filepath]:
            self._load_sound(filepath)
        return self._sfx[filepath]

_sound_loader = SoundLoader()
get_sfx = _sound_loader.get_sfx
