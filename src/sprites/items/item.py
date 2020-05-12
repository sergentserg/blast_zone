import random
import pytweening as tween
import pygame as pg
from pygame.math import Vector2 as vec
from itertools import chain

from src.sprites.spriteW import SpriteW
import src.utility.sound_loader as sfx_loader

# Credits to Chris Bradfield from KidsCanCode for the item bobbing animation.

class ItemBox(SpriteW):
    DISAPPEAR_ALPHA = [alpha for alpha in range(175, 255, 15)]
    SFX = 'box.wav'
    def __init__(self, x, y, max_durability, image, groups):
        SpriteW.__init__(self, x, y, image,
                        (groups['item_boxes'], groups['obstacles'], groups['all']))
        # Protects original image from being changed.
        self.image = self.image.copy()
        self.groups = groups
        self._box_sfx = sfx_loader.get_sfx(ItemBox.SFX)
        self._durability = max_durability
        self._disappear_alpha = chain(ItemBox.DISAPPEAR_ALPHA * 2)

    def wear_out(self):
        # Wears out the box or destroys it.
        self._durability -= 1
        for i in range(10):
            self._darken(255)

    def is_broken(self):
        return self._durability == 0

    def _darken(self, alpha):
        self.image.fill((255, 255, 255, 255),
                                    special_flags=pg.BLEND_RGBA_MULT)

    def update(self, dt):
        # Box breaks at 0 durability.
        if self.is_broken():
            try:
                _darken(self, next(self._disappear_alpha))
            except:
                # Spawn an item.
                item_type = random.choice([HealthItem, AmmoItem, SpeedItem])
                item_type(self.rect.centerx, self.rect.centery, self.groups)
                self._box_sfx.play()
                self.kill()


class WoodenBox(ItemBox):
    IMAGE = 'crateWood.png'
    MAX_DURABILITY = 2
    SPAWN_RATE = 0.2
    def __init__(self, x, y, groups):
        ItemBox.__init__(self, x, y, WoodenBox.MAX_DURABILITY, WoodenBox.IMAGE, groups)


class MetalBox(ItemBox):
    IMAGE = 'crateMetal.png'
    MAX_DURABILITY = 4
    def __init__(self, x, y, groups):
        ItemBox.__init__(self, x, y, MetalBox.MAX_DURABILITY, MetalBox.IMAGE, groups)


class Item(SpriteW):
    # Number of pixels up and down that item will bob.
    BOB_RANGE = 15
    BOB_SPEED = 0.2
    def __init__(self, x, y, image, sound, groups):
        SpriteW.__init__(self, x, y, image, (groups['all'], groups['items']))
        self.sfx = sfx_loader.get_sfx(sound)
        # Tween function maps integer steps to values between 0 and 1.
        self.spawn_pos = vec(x, y)
        self.tween = tween.easeInOutSine
        self.step = 0
        self.direction = 1

    def update(self, dt):
        # Shift bobbing y offset to bob about item's original center.
        offset = Item.BOB_RANGE * (self.tween(self.step / Item.BOB_RANGE) - 0.5)
        self.rect.centery = self.spawn_pos.y + offset * self.direction
        self.step += Item.BOB_SPEED
        # Reverse bobbing direction when item returns to center.
        if self.step > Item.BOB_RANGE:
            self.step = 0
            self.direction *= -1

    def kill(self):
        self.sfx.play()
        super().kill()


class HealthItem(Item):
    IMAGE = 'health_item.png'
    SFX  = 'heal.wav'
    def __init__(self, x, y, groups):
        Item.__init__(self, x, y, HealthItem.IMAGE, HealthItem.SFX, groups)

    def apply_effect(self, tank):
        min_pct, max_pct = 0.1, 0.2
        pct = min_pct + random.random() * (max_pct - min_pct)
        tank.heal(pct)
        super().kill()


class AmmoItem(Item):
    IMAGE = 'ammo_item.png'
    SFX = 'reload.wav'
    def __init__(self, x, y, groups):
        Item.__init__(self, x, y, AmmoItem.IMAGE, AmmoItem.SFX, groups)

    def apply_effect(self, tank):
        tank.reload()
        super().kill()


class SpeedItem(Item):
    IMAGE = 'speed_item.png'
    SFX = 'speedup.wav'
    def __init__(self, x, y, groups):
        Item.__init__(self, x, y, SpeedItem.IMAGE, SpeedItem.SFX, groups)

    def apply_effect(self, tank):
        min_speed, max_speed = 200, 500
        boost = min_speed + random.random() * (max_speed - min_speed)
        tank.vel += vec(boost, 0).rotate(-tank.rot)
        super().kill()


def spawn_box(x, y, groups):
    if random.random() < WoodenBox.SPAWN_RATE:
        WoodenBox(x, y, groups)
    else:
        MetalBox(x, y, groups)
