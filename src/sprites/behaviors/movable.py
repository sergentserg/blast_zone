import pygame as pg

import src.config as cfg
from src.sprites.spriteW import SpriteW, collide_hit_rect
vec = pg.math.Vector2


class Movable:
    def __init__(self, x, y):
        self.pos = vec(x, y)
        self.vel = vec(0, 0)

    def move(self, dt):
        # By default, Movable objects like bullets ignore colliders.
        self.pos += self.vel * dt
        self.rect.center = self.pos
        self.hit_rect.center = self.pos

class MovableNonlinear(Movable):
    SPEED_CUTOFF = 0
    def __init__(self, x, y):
        Movable.__init__(self, x, y)
        self.acc = vec(0, 0)
        self._hit_wall = False

    # @override
    def move(self, collider_groups, dt):
        # Simulate friction.
        self.acc -= 4*self.vel

        # Effect kinematic equations.
        self.vel += self.acc * dt
        if self.vel.length_squared() < self.SPEED_CUTOFF:
            self.vel.x = 0
            selv.vel.y = 0
        else:
            displacement = (self.vel * dt) + (0.5 * self.acc * dt**2)
            self._handle_colliders(displacement, collider_groups)

    def _handle_colliders(self, displacement, collider_group):
        self._hit_wall = False
        # Collision in x direction.
        self.pos.x += displacement.x
        self.hit_rect.centerx = self.pos.x
        collider = pg.sprite.spritecollideany(self, collider_group, collide_hit_rect)

        if collider:
            # self.pos.x -= displacement.x
            if self.pos.x < collider.rect.centerx:
                self.pos.x = collider.rect.left - self.hit_rect.width / 2
            else:
                self.pos.x = collider.rect.right + self.hit_rect.width / 2
            self.vel.x = 0
            self.hit_rect.centerx = self.pos.x
            self._hit_wall = True

        # Collision in y direction.
        self.pos.y += displacement.y
        self.hit_rect.centery = self.pos.y
        collider = pg.sprite.spritecollideany(self, collider_group, collide_hit_rect)

        if collider:
            # self.pos.y -= self.vel.y
            # Hit top of collider.
            if self.pos.y < collider.rect.centery:
                self.pos.y = collider.rect.top - self.hit_rect.height / 2
            # Hit bottom of collider.
            else:
                self.pos.y = collider.rect.bottom + self.hit_rect.height / 2
            self.vel.y = 0
            self.hit_rect.centery = self.pos.y
            self._hit_wall = True
            
        self.rect.center = self.pos

    def collided_with_wall(self):
        return self._hit_wall
