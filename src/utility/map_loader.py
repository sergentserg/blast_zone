# Tilemap Demo from KidsCanCode.
# Augmented to initialize sprites based on tm object locations.
from os import path
import pygame as pg
import pytmx

import src.config as cfg
from src.sprites.tank import ColorTank, LargeTank, BigTank, HugeTank
import src.sprites.obstacles as obstacles
import src.sprites.item as item
from src.entities.turret_ctrl import TurretCtrl
from src.entities.tank_ctrl import AITankCtrl
from src.sprites.barrel import Turret

class TiledMapLoader:
    def make_map(self, filename):
        self._load_map(filename)
        temp_surface = pg.Surface((self._width, self._height))
        self._render(temp_surface)
        return temp_surface

    def _load_map(self, filename):
        tm = pytmx.load_pygame(path.join(cfg.MAP_DIR, filename),
                                pixelalpha = True)
        self._width = tm.width * tm.tilewidth
        self._height = tm.height * tm.tileheight
        self._tmxdata = tm #stores data for later access

    def _render(self, surface):
        ti = self._tmxdata.get_tile_image_by_gid
        for layer in self._tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self._tmxdata.tilewidth,
                                    y * self._tmxdata.tileheight))
        surface = surface.convert_alpha()
        surface.set_colorkey(cfg.BLACK)

    def init_sprites(self, groups, player, ai_mobs):
        ai_path_data = []
        ai_turret_data = []
        for obj in self._tmxdata.objects:
            if obj.name == 'player_start':
                player.tank = ColorTank(obj.x, obj.y, obj.color, obj.type, groups)
                # player.tank = HugeTank(obj.x, obj.y, groups)
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

        # Spawn enemy AI tank and provide path information.
        ai_path_data.sort(key=lambda point: point.path_index)
        tank = LargeTank(ai_tank.x, ai_tank.y, groups)
        tank_ctrl = AITankCtrl(tank, ai_path_data, player.tank)
        ai_mobs.append(tank_ctrl)

        # Spawn all turrets.
        for t in ai_turret_data:
            turret = Turret(t.x, t.y, t.type, t.style, groups)
            ai_mobs.append(TurretCtrl(turret, player.tank, tank_ctrl))


_map_loader = TiledMapLoader()

init_sprites = _map_loader.init_sprites
make_map =  _map_loader.make_map
