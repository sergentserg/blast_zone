from random import choice, random
from pygame.math import Vector2 as vec

from src.sprites.spriteW import SpriteW
import src.utility.sound_loader as sfx_loader

class Item(SpriteW):
    _IMAGES = ['crateWood.png', 'crateMetal.png']
    EFFECTS = ['heal', 'ammo', 'speedup']
    def __init__(self, x, y, groups):
        SpriteW.__init__(self, x, y, choice(Item._IMAGES),
                        (groups['items'], groups['all']))
        self.item_sfx = {'ammo': sfx_loader.get_sfx('reload.wav'),
                            'heal': sfx_loader.get_sfx('heal.wav'),
                            'speedup': sfx_loader.get_sfx('speedup.wav')}

    def apply_effect(self, tank):
        item_effect = choice(Item.EFFECTS)
        if item_effect == 'heal':
            self._heal(tank)
        elif item_effect == 'ammo':
            self._reload(tank)
        elif item_effect == 'speedup':
            self._speedup(tank)
        self.kill()

    def _heal(self, tank):
        min_pct, max_pct = 0.1, 0.2
        pct = min_pct + random() * (max_pct - min_pct)
        self.item_sfx['heal'].play()
        tank.health += tank.MAX_HEALTH * pct
        if tank.health > 100:
            tank.health = 100

    def _reload(self, tank):
        self.item_sfx['ammo'].play()
        tank.reload()

    def _speedup(self, tank):
        min_speed, max_speed = 200, 500
        boost = min_speed + random() * (max_speed - min_speed)
        tank.vel += vec(boost, 0).rotate(-tank.rot)
        self.item_sfx['speedup'].play()
