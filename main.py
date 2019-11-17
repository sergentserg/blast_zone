import pygame as pg
import random
import src.settings as cfg
import os
from src.maps.tilemap import level1
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
        self.game_dir = os.path.dirname(__file__)
        self.img_dir = os.path.join(self.game_dir, "img")
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
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.map_img = level1.make_map()
        self.map_rect = self.map_img.get_rect()
        self.input_state = input_manager.input_state
        self.main_menu = Menu(*self.screen.get_rect())
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

        self.input_state.update()
        # if self.input_state.get_mousestate(0) == input_manager.InputState.JUST_PRESSED:
        #     mouse_X, mouse_Y = pg.mouse.get_pos()
        #     self.button.handle_input(mouse_X, mouse_Y, self.t)


    def update(self, dt):
        """  update(): Updates sprites in every group """
        self.all_sprites.update(dt)

    def render(self):
        """ render(): Draw and display sprites and other graphics
        onto screen

        """
        self.screen.fill(cfg.BLACK)
        self.screen.blit(self.main_menu.img, self.main_menu.rect)
        self.all_sprites.draw(self.screen)
        pg.display.flip()


g = Game()
while g.running:
    g.new()
pg.quit()
