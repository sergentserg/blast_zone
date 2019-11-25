import pygame as pg
import random
import src.settings as cfg
import os
from src.utility.tilemap import level1
import src.input.input_manager as input_manager
from src.ui.menu import Menu
from src.ui.buttons import Button

class Game:
    def __init__(self):
        """
        __init__: Initializes pygame modules and creates a screen and Clock.

        """
        self.screen = pg.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        pg.display.set_caption(cfg.TITLE)
        self.clock = pg.time.Clock()
        # Used to keep pygame running
        self.running = True

        # for object in object_layer:
        #     if object.name == "player":
        #         Player(object.x, object.y, turretFileName)

    def new(self):
        """
        new(): Creates a new set of sprites for the current game run, and
        starts up the game

        """
        self.input_state = input_manager.input_state
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.map_img = level1.make_map()
        self.map_rect = self.map_img.get_rect()
        self.menu = Menu()
        self.run()

    def run(self):
        """ run(): Runs game loop: sets frame rate, processes inputs,
        updates sprites, and renders

        """
        # Used to continue game loop
        self.playing = True
        self.t = 0
        while self.playing:
            self.dt = self.clock.tick(cfg.FPS) / 1000
            self.t += self.dt
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
            elif event.type == pg.MOUSEMOTION:
                # -1 indicates no button press at all
                self.menu.handle_mouse(self.dt, -1)
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    print("Flagged for review.\n\n\n")

        self.input_state.update()
        self.menu.handle_mouse(self.dt, self.input_state.get_mousestate(0))


    def update(self, dt):
        """  update(): Updates sprites in every group """
        self.all_sprites.update(dt)


    def render(self):
        """ render(): Draw and display sprites and other graphics
        onto screen

        """
        self.screen.fill(cfg.BLACK)
        self.all_sprites.draw(self.screen)
        self.menu.draw(self.screen)
        pg.display.flip()

g = Game()
while g.running:
    g.new()
pg.quit()
