import pygame as pg
import random
import settings as cfg
import os

class Game:
    def __init__(self):
        """
        __init__: Initializes pygame modules and creates a screen and Clock.

        """
        pg.init()
        self.screen = pg.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        pg.display.set_caption(cfg.TITLE)
        self.game_dir = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.game_dir, "img")
        self.clock = pg.time.Clock()
        # Used to keep pygame running
        self.running = True

    def new(self):
        """
        new(): Creates a new set of sprites for the current game run, and
        starts up the game

        """
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.run()

    def run(self):
        """ run(): Runs game loop: sets frame rate, processes inputs,
        updates sprites, and renders

        """
        # Used to continue game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(cfg.FPS) / 1000
            self.process_inputs()
            self.update(self.dt)
            self.render()

    def process_inputs(self):
        """ Process user-inputs from the keyboard and mouse """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self, dt):
        """  update(): Updates sprites in every group """
        self.all_sprites.update(dt)

    def render(self):
        """ render(): Draw and display sprites and other graphics
        onto screen

        """
        self.screen.fill(cfg.BLACK)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


g = Game()
while g.running:
    g.new()
pg.quit()
