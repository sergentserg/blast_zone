import pygame as pg
import random

import src.utility.map_loader as map_loader
from src.utility.timer import Timer
from src.sprites.item import spawn_box
from src.sprites.obstacles import BoundaryWall
from src.sprites.camera import Camera
from src.sprites.effects.explosion import Explosion
from src.sprites.spriteW import bullet_collide_id, collide_hit_rect

vec = pg.math.Vector2


class Level:
    MAX_ITEMS = 1
    ITEM_RESPAWN_TIME = 5000
    def __init__(self, level_file, player, game_state):
        self._game_state = game_state
        self._score = 0
        self.image = map_loader.make_map(level_file)
        self.rect = self.image.get_rect()
        self._groups = {'all': pg.sprite.LayeredUpdates(),
                        'tanks': pg.sprite.Group(),
                        'damageable': pg.sprite.Group(),
                        'bullets': pg.sprite.Group(),
                        'obstacles': pg.sprite.Group(),
                        'items': pg.sprite.Group(),
                        'item_boxes': pg.sprite.Group()}
        self._ai_mobs = []
        map_loader.init_sprites(self._groups, player, self._ai_mobs)
        self._player = player

        self._camera = Camera(player, self.rect.width, self.rect.height)
        player.camera = self._camera

        # Top/Bottom boundaries.
        BoundaryWall(0, 0, self.rect.width, 1, self._groups)
        BoundaryWall(0, self.rect.height, self.rect.width, 1, self._groups)
        # Left/Right boundaries.
        BoundaryWall(0, 0, 1, self.rect.height, self._groups)
        BoundaryWall(self.rect.width, 0, 1, self.rect.height, self._groups)

        self._item_timer = Timer()
        self.level_music = None

    def _can_spawn_item(self):
        return self._item_timer.elapsed_time() > Level.ITEM_RESPAWN_TIME

    def update(self, dt):
        self._groups['all'].update(dt)
        # Update list of ai mobs.
        for ai in self._ai_mobs:
            ai.update(dt)
        self._camera.update()

        # Handle damage-causing bullets.
        hits = pg.sprite.groupcollide(self._groups['damageable'],
                                        self._groups['bullets'], False, True,
                                        bullet_collide_id)

        for sprite, bullets in hits.items():
            for bullet in bullets:
                Explosion(bullet.pos.x, bullet.pos.y, self._groups)
                sprite.damage(bullet.damage)
                if sprite.health <= 0:
                    sprite.kill()
                    if not self._player.alive():
                        self._game_state.game_over()
                    else:
                        self._ai_mobs = [ai for ai in self._ai_mobs if ai.alive()]
                        if len(self._ai_mobs) == 0:
                            self._game_state.game_over()
                    break

        # Handle bullets that destroy item boxes.
        for box in self._groups['item_boxes']:
            if not box.is_broken():
                for bullet in self._groups['bullets']:
                    if collide_hit_rect(box, bullet):
                        bullet.kill()
                        box.wear_out()
                        if box.is_broken():
                            self._item_timer.restart()
                            break

        # See if it's time to spawn a new item.
        if len(self._groups['item_boxes']) < Level.MAX_ITEMS and self._can_spawn_item():
            spawn_box(self._groups)


        # Handle bullets that hit other obstacles.
        hits = pg.sprite.groupcollide(self._groups['bullets'],
                                        self._groups['obstacles'], True, False,
                                                bullet_collide_id)

        # Handle item pick-up.
        hits = pg.sprite.groupcollide(self._groups['tanks'],
                                        self._groups['items'], False, False)
        for tank, items in hits.items():
            for item in items:
                tank.pickup(item)
                # item.apply_effect(tank)

        # Tank/tank collision.
        all_tanks = list(self._groups['tanks'])
        for i in range(0, len(all_tanks)):
            tank_a = all_tanks[i]
            for tank_b in all_tanks[i + 1:]:
                if collide_hit_rect(tank_a, tank_b):
                    knockback_dir = tank_b.rot
                    tank_a.vel += vec(tank_b.KNOCKBACK, 0).rotate(knockback_dir)
                    tank_b.vel -= vec(tank_b.KNOCKBACK, 0).rotate(knockback_dir)

    def draw(self, screen):
        screen.blit(self.image, self._camera.apply(self.rect))
        # self._groups['all'].draw(screen)
        for sprite in self._groups['all']:
            screen.blit(sprite.image, self._camera.apply(sprite.rect))
            # pg.draw.rect(screen, (255, 255, 255), self._camera.apply(sprite.hit_rect), 1)
        for ai in self._ai_mobs:
            ai.draw_health(screen, self._camera)
        self._player.draw_hud(screen, self._camera)
        # for tank in self._groups['tanks']:
        #     tank.draw_health(screen, self._camera)
