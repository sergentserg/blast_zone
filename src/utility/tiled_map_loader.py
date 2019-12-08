#Tilemap Demo from KidsCanCode
import pygame as pg
import pytmx
import sys
from os import path
from src.settings import *
from ..sprites.spriteW import SpriteW
from src.sprites.tanks.color_tank import ColorTank
from src.sprites.barrels.barrel_factory import BarrelFactory

class TiledMapLoader:
    def __load_map(self, filename):
        tm = pytmx.load_pygame(path.join(MAP_DIR, filename), pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm #stores data for later access

    def __render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def init_sprites(self, groups, player):
        for tile_object in self.tmxdata.objects:
            if tile_object.name == 'player_start':
                player.set_tank(ColorTank(tile_object.x, tile_object.y, tile_object.color, groups))

    def make_map(self, filename):
        self.__load_map(filename)
        temp_surface = pg.Surface((self.width, self.height))
        temp_surface.set_colorkey(BLACK)
        self.__render(temp_surface)
        return temp_surface
