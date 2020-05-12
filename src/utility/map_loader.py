# Tilemap Demo from KidsCanCode.
# Augmented to initialize sprites based on tm object locations.
from os import path
import pygame as pg
import pytmx
import sys

import src.config as cfg
from src.sprites.tanks.color_tank import ColorTank
import src.sprites.misc.obstacles as obstacles
import src.sprites.items.item as item
from src.entities.turret_ctrl import TurretCtrl
from src.entities.tank_ctrl import AITankCtrl

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

    def init_sprites(self, groups, player, ai_mobs):
        ai_path_data = []
        ai_turret_data = []
        for obj in self.tmxdata.objects:
            if obj.name == 'player_start':
                player.set_tank(ColorTank(obj.x, obj.y, obj.color, groups))
            if obj.name == 'smallTree':
                obstacles.Tree(obj.x, obj.y, groups)
            if obj.name == 'AIPatrolPoint':
                ai_path_data.append(obj)
            if obj.name == 'box':
                item.spawn_box(obj.x, obj.y, groups)
            if obj.name == 'turret':
                ai_turret_data.append(obj)
            if obj.name == 'enemyTank':
                ai_tank = obj
        # Spawn player tank.

        # Spawn enemy AI tank and provide path information.
        ai_path_data.sort(key=lambda point: point.path_index)
        ai_mobs.append(AITankCtrl(ai_tank.x, ai_tank.y, player.tank, ai_path_data, ai_tank.color, groups))

        # Spawn all turrets.
        for t in ai_turret_data:
            ai_mobs.append(TurretCtrl(t.x, t.y, player.tank, t.type, t.style, groups))


    def make_map(self, filename):
        self._load_map(filename)
        temp_surface = pg.Surface((self.width, self.height))
        self._render(temp_surface)
        return temp_surface

_map_loader = TiledMapLoader()

init_sprites = _map_loader.init_sprites
make_map =  _map_loader.make_map
