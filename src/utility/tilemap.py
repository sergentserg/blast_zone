#Tilemap Demo from KidsCanCode
import pygame as pg
import pytmx
import sys
from os import path
from src.settings import *
from ..sprites.spriteW import SpriteW
from src.sprites.barrels.barrel_factory import BarrelFactory

class TiledMap:
    def __init__(self, filename):
        map_dir = path.join(GAME_DIR, 'maps')
        tm = pytmx.load_pygame(path.join(map_dir, filename), pixelalpha = True)
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

    def init_sprites(self, groups):
        for tile_object in self.tmxdata.objects:
            if tile_object.type == 'barrel':
                BarrelFactory.create_barrel(tile_object, groups)

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.__render(temp_surface)
        return temp_surface

level1 = TiledMap("level_1.tmx")
