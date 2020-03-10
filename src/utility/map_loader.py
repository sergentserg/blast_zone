# Tilemap Demo from KidsCanCode.
# Augmented to initialize sprites based on tm object locations.
from os import path
import pygame as pg
import pytmx
import sys

import src.config as cfg
from src.sprites.tanks.color_tank import ColorTank
import src.sprites.misc.obstacles as obs
import src.sprites.items.item as item

class TiledMapLoader:
    def _load_map(self, filename):
        tm = pytmx.load_pygame(path.join(cfg.MAP_DIR, filename),
                                pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm #stores data for later access

    def _render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                    y * self.tmxdata.tileheight))
        surface = surface.convert_alpha()
        surface.set_colorkey(cfg.BLACK)

    def init_sprites(self, groups, player):
        for obj in self.tmxdata.objects:
            if obj.name == 'player_start':
                player.set_tank(ColorTank(obj.x, obj.y, obj.color, groups))
            if obj.name == 'smallTree':
                obs.Tree(obj.x, obj.y, groups)
            if obj.name == 'box':
                item.Item(obj.x, obj.y, groups)

    def make_map(self, filename):
        self._load_map(filename)
        temp_surface = pg.Surface((self.width, self.height))
        self._render(temp_surface)
        return temp_surface

_map_loader = TiledMapLoader()

init_sprites = _map_loader.init_sprites
make_map =  _map_loader.make_map
