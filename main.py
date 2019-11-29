import pygame as pg
import random
import src.settings as cfg
import os
from src.utility.tilemap import level1
import src.input.input_manager as input_manager
from src.utility.game_text import text_renderer

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
        level1.init_sprites(self.all_sprites)
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
        self.input_state.update()


    def update(self, dt):
        """  update(): Updates sprites in every group """
        self.all_sprites.update(dt)


    def render(self):
        """ render(): Draw and display sprites and other graphics
        onto screen

        """
        self.screen.fill(cfg.BLACK)
        self.screen.blit(self.map_img, self.map_rect)
        self.all_sprites.draw(self.screen)
        # for sprite in self.all_sprites:
        #     pg.draw.rect(self.screen, (255, 255, 255), sprite.rect, 1)
        pg.display.set_caption(" ".join([cfg.TITLE, " FPS: ", str(int(self.clock.get_fps()))]))
        pg.display.flip()

g = Game()
while g.running:
    g.new()
pg.quit()
