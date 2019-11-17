import pygame as pg
import pytmx
from os import path

maps_dir = path.dirname(__file__)

# Thanks to Chris Bradfield
class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def __render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

        for tile_object in self.tmxdata.objects:
            if tile_object.name == 'woodbox':
                print('A wooden box')

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.__render(temp_surface)
        return temp_surface

level1 = TiledMap(path.join(maps_dir, 'level_1.tmx'))
