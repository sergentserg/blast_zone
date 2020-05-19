import pygame as pg

import src.config as cfg


class Timer:
    def __init__(self):
        self._pause_time = 0
        self._unpause_time = pg.time.get_ticks()
        self._time = 0
        self._paused = False

    def pause(self):
        self._paused = True
        self._pause_time += cfg.time_since(self._unpause_time)

    def unpause(self):
        self._paused = False
        self._unpause_time = pg.time.get_ticks()

    def get_seconds(self):
        total_secs = self._pause_time
        if not self._paused:
            total_secs += cfg.time_since(self._unpause_time)
        return total_secs // 1000
