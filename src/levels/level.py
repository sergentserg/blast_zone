import pygame as pg

from src.sprites.misc.obstacles import BoundaryWall
import src.utility.map_loader as map_loader
from src.sprites.camera import Camera
from src.sprites.effects.explosion import Explosion
from src.sprites.spriteW import bullet_collide_id

class Level:
    def __init__(self, level_file, player):
        self.level_file = level_file
        self.image = map_loader.make_map(self.level_file)
        self.rect = self.image.get_rect()

        self.groups = {'all': pg.sprite.LayeredUpdates(),
                        'tanks': pg.sprite.Group(),
                        'bullets': pg.sprite.Group(),
                        'obstacles': pg.sprite.Group(),
                        'items': pg.sprite.Group()}
        self.turrets = []
        map_loader.init_sprites(self.groups, player, self.turrets)
        for turret in self.turrets:
            turret.target = player.tank

        self.camera = Camera(player, self.rect.width, self.rect.height)
        player.camera = self.camera

        # Top/Bottom boundaries.
        BoundaryWall(0, 0, self.rect.width, 1, self.groups)
        BoundaryWall(0, self.rect.height, self.rect.width, 1, self.groups)
        # Left/Right boundaries.
        BoundaryWall(0, 0, 1, self.rect.height, self.groups)
        BoundaryWall(self.rect.width, 0, 1, self.rect.height, self.groups)

        self.level_music = None

    def update(self, dt):
        self.groups['all'].update(dt)
        for turret in self.turrets:
            turret.update(dt)
        self.camera.update()

        # Bullet hits obstacle.
        hits = pg.sprite.groupcollide(self.groups['bullets'],
                                        self.groups['obstacles'], True, False,
                                                bullet_collide_id)

        # Item collision.
        hits = pg.sprite.groupcollide(self.groups['tanks'],
                                        self.groups['items'], False, False)
        for tank, items in hits.items():
            for item in items:
                item.apply_effect(tank)

        # Bullet/Tank collision
        hits = pg.sprite.groupcollide(self.groups['tanks'],
                                        self.groups['bullets'], False, True,
                                        bullet_collide_id)
        for tank, bullets in hits.items():
            for bullet in bullets:
                Explosion(bullet.pos.x, bullet.pos.y, self.groups)
                tank.health -= bullet.stats["damage"]
                if tank.health <= 0:
                    tank.kill()
                    break

    def draw(self, screen):
        screen.blit(self.image, self.camera.apply(self.rect))
        # self.groups['all'].draw(screen)
        for sprite in self.groups['all']:
            screen.blit(sprite.image, self.camera.apply(sprite.rect))
            # pg.draw.rect(screen, (255, 255, 255), self.camera.apply(sprite.hit_rect), 1)
        for tank in self.groups['tanks']:
            tank.draw_health(screen, self.camera)
