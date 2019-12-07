import pygame as pg
import random
import src.settings as cfg
import os
from src.utility.tilemap import level1
import src.input.input_state as input_state
from src.utility.game_text import text_renderer
from src.entities.player_ctrl import PlayerCtrl

class Game:
    def __init__(self):
        """
        __init__: Initializes pygame modules and creates a screen and Clock.

        """
        # Screen for drawing game objects
        self.screen = pg.display.set_mode((cfg.SCREEN_WIDTH, cfg.SCREEN_HEIGHT))
        pg.display.set_caption(cfg.TITLE)

        # Clock object for time functions
        self.clock = pg.time.Clock()
        # Used to keep pygame running
        self.running = True

    def new(self):
        """
        new(): Creates a new set of sprites for the current game run, and
        starts up the game

        """
        self.input_state = input_state.input_state
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player = PlayerCtrl(cfg.SCREEN_WIDTH/2, cfg.SCREEN_HEIGHT/2, "blue", self.all_sprites)
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
        self.player.handle_input(self.input_state, dt)
        self.all_sprites.update(dt)
        # Handle collisions

    def render(self):
        """ render(): Draw and display sprites and other graphics
        onto screen

        """
        # Clear the screen
        self.screen.fill(cfg.BLACK)
        self.screen.blit(self.map_img, self.map_rect)
        self.all_sprites.draw(self.screen)
        # for sprite in self.all_sprites:
        #     pg.draw.rect(self.screen, (255, 255, 255), sprite.rect, 1)
        pg.display.set_caption(" ".join([cfg.TITLE, " FPS: ", str(int(self.clock.get_fps()))]))
        pg.display.flip()

    def quit(self):
        pg.quit()
