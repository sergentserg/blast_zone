import pygame as pg
import random

import src.utility.map_loader as map_loader
from src.sprites.items.item import spawn_box
from src.sprites.misc.obstacles import BoundaryWall
from src.sprites.camera import Camera
from src.sprites.effects.explosion import Explosion
from src.sprites.spriteW import bullet_collide_id, collide_hit_rect
from src.sprites.tanks.tank import Tank

vec = pg.math.Vector2


class Level:
    MAX_ITEMS = 1
    ITEM_RESPAWN_TIME = 5000
    def __init__(self, level_file, player):
        self.level_file = level_file
        self.image = map_loader.make_map(self.level_file)
        self.rect = self.image.get_rect()
        self.groups = {'all': pg.sprite.LayeredUpdates(),
                        'tanks': pg.sprite.Group(),
                        'damageable': pg.sprite.Group(),
                        'bullets': pg.sprite.Group(),
                        'obstacles': pg.sprite.Group(),
                        'items': pg.sprite.Group(),
                        'item_boxes': pg.sprite.Group()}
        self.ai_mobs = []
        map_loader.init_sprites(self.groups, player, self.ai_mobs)
        for ai in self.ai_mobs:
            ai.target = player.tank

        self.camera = Camera(player, self.rect.width, self.rect.height)
        player.camera = self.camera

        # Top/Bottom boundaries.
        BoundaryWall(0, 0, self.rect.width, 1, self.groups)
        BoundaryWall(0, self.rect.height, self.rect.width, 1, self.groups)
        # Left/Right boundaries.
        BoundaryWall(0, 0, 1, self.rect.height, self.groups)
        BoundaryWall(self.rect.width, 0, 1, self.rect.height, self.groups)

        self.item_destroyed_time = pg.time.get_ticks()
        self.level_music = None

    def _can_spawn_item(self):
        return (pg.time.get_ticks() - self.item_destroyed_time) > Level.ITEM_RESPAWN_TIME

    def update(self, dt):
        self.groups['all'].update(dt)
        # Update list of ai mobs.
        self.ai_mobs = [ai for ai in self.ai_mobs if ai.alive()]
        for ai in self.ai_mobs:
            ai.update(dt)
        self.camera.update()

        # Handle damage-causing bullets.
        hits = pg.sprite.groupcollide(self.groups['damageable'],
                                        self.groups['bullets'], False, True,
                                        bullet_collide_id)

        for sprite, bullets in hits.items():
            for bullet in bullets:
                Explosion(bullet.pos.x, bullet.pos.y, self.groups)
                sprite.health -= bullet.stats["damage"]
                if sprite.health <= 0:
                    sprite.kill()
                    break

        # Handle bullets that destroy item boxes.
        for box in self.groups['item_boxes']:
            if not box.is_broken():
                for bullet in self.groups['bullets']:
                    if collide_hit_rect(box, bullet):
                        bullet.kill()
                        box.wear_out()
                        if box.is_broken():
                            self.item_destroyed_time = pg.time.get_ticks()
                            break

        # See if it's time to spawn a new item.
        if len(self.groups['item_boxes']) < Level.MAX_ITEMS and self._can_spawn_item():
            x = random.randint(0, self.rect.width)
            y = random.randint(0, self.rect.height)
            spawn_box(x, y, self.groups)


        # Handle bullets that hit other obstacles.
        hits = pg.sprite.groupcollide(self.groups['bullets'],
                                        self.groups['obstacles'], True, False,
                                                bullet_collide_id)

        # Handle item pick-up.
        hits = pg.sprite.groupcollide(self.groups['tanks'],
                                        self.groups['items'], False, False)
        for tank, items in hits.items():
            for item in items:
                item.apply_effect(tank)

        # Tank/tank collision.
        all_tanks = list(self.groups['tanks'])
        for i in range(0, len(all_tanks)):
            tank_a = all_tanks[i]
            for tank_b in all_tanks[i + 1:]:
                if collide_hit_rect(tank_a, tank_b):
                    knockback_dir = tank_b.rot
                    tank_a.vel += vec(Tank.KNOCKBACK, 0).rotate(knockback_dir)
                    tank_b.vel -= vec(Tank.KNOCKBACK, 0).rotate(knockback_dir)

    def draw(self, screen):
        screen.blit(self.image, self.camera.apply(self.rect))
        # self.groups['all'].draw(screen)
        for sprite in self.groups['all']:
            screen.blit(sprite.image, self.camera.apply(sprite.rect))
            # pg.draw.rect(screen, (255, 255, 255), self.camera.apply(sprite.hit_rect), 1)
        for ai in self.ai_mobs:
            ai.draw_health(screen, self.camera)
        # self.player.draw_health(screen, self.camera)
        # for tank in self.groups['tanks']:
        #     tank.draw_health(screen, self.camera)
