import pygame as pg

import src.config as cfg


class Timer:
    timers = []
    @classmethod
    def pause_timers(cls):
        for timer in cls.timers:
            timer.pause()

    @classmethod
    def unpause_timers(cls):
        for timer in cls.timers:
            timer.unpause()

    def __init__(self):
        self._elapsed_time = 0
        self.unpause()
        Timer.timers.append(self)

    def pause(self):
        self._paused = True
        self._elapsed_time += cfg.time_since(self._unpause_time)
        # self._elapsed_time += pg.time.get_ticks()

    def unpause(self):
        self._paused = False
        self._unpause_time = pg.time.get_ticks()

    def restart(self):
        self._elapsed_time = 0
        self._unpause_time = pg.time.get_ticks()

    def elapsed_time(self):
        millisecs = self._elapsed_time
        if not self._paused:
            millisecs += cfg.time_since(self._unpause_time)
        return millisecs
        # return self._elapsed_time + (not self._paused) * cfg.time_since(self._unpause_time)
