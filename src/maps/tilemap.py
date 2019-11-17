#Tilemap Demo from KidsCanCode
import pygame as pg
import pytmx
import sys
from os import path
from ..settings import *
from ..sprites.spriteW import SpriteW

class TiledMap:
    def __init__(self, filename):
        map_dir = path.dirname(__file__)
        tm = pytmx.load_pygame(path.join(map_dir, filename), pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm #stores data for later access

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x*self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self): #Creates surface to draw map on
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

level1 = TiledMap("level_1.tmx")
