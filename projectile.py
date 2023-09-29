import pygame
import math
from settings import *
from colors import *
from src.animator import *

from random import randint, choice

PROJECTILE_DESPAWN_TIMER = 10
class ProjectileKind():
    def __init__(self, type, texture, scale):
        self.type = type
        self.scale = scale
        self.texture = texture
        
class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, pos, angle, speed, kind, dt):
        super().__init__(group)
        self.angle = angle
        self.kind = kind
        self.type = self.kind.type
        if self.type == SPRITE_TYPE_ASTEROID:
            self.unrotated_image = pygame.transform.scale_by(self.kind.texture, self.kind.scale)
        elif self.type == SPRITE_TYPE_BULLET:
            self.unrotated_image = pygame.transform.scale_by(self.kind.texture, self.kind.scale)
        
        self.unrotated_rect = self.unrotated_image.get_rect(center = pos)
        self.image = self.unrotated_image
        self.rect = self.image.get_rect(center = pos)
        self.rotate_image()

        self.speed = speed
        self.dx = math.sin(self.angle) * self.speed * dt
        self.dy = math.cos(self.angle) * self.speed * dt
        self.dt = dt

        self.despawn_timer = PROJECTILE_DESPAWN_TIMER

    def rotate_image(self):
        self.image = pygame.transform.rotate(self.unrotated_image, self.angle * 180 / math.pi)
        self.image.set_colorkey(black)
        self.rect.centerx = self.unrotated_rect.centerx - (self.image.get_width() // 2)
        self.rect.centery = self.unrotated_rect.centery - (self.image.get_height() // 2)
    
    def destroy(self):
        if self.despawn_timer > 0:
            self.despawn_timer -= self.dt
        else:
            self.kill()
     
    def update(self):

        self.unrotated_rect.x += self.dx
        self.unrotated_rect.y += self.dy

        if self.type == SPRITE_TYPE_ASTEROID:
            self.angle += self.dt * self.dt *  self.speed
            self.angle %= (2 * math.pi)
            self.rotate_image()
        else:
            self.rect.x = self.unrotated_rect.x
            self.rect.y = self.unrotated_rect.y

        self.destroy()

class ProjectileManager:
    def __init__(self):
        self.animtor = Animator('./graphics/asteroid_spritesheet_outline.png', 32, 1, 3, (0, 0))

        self.animtor.add('asteroid1', 1, 1, 1)
        self.animtor.add('asteroid2', 1, 2, 2)
        self.animtor.add('asteroid3', 1, 3, 3)

        self.lazer_sprite = pygame.image.load('./graphics/lazer.png').convert_alpha()

    def spawn_asteroid(self, camera, scale, a_pos, player, dt):
        at_pos = pygame.math.Vector2(a_pos)
        player_pos = pygame.math.Vector2(player)
        angle = math.atan2(at_pos.y - player_pos.y , at_pos.x - player_pos.x)
        rand_speed = randint(100, 300)
        rand_sprite = choice(['asteroid1', 'asteroid2', 'asteroid3'])
        self.animtor.play(rand_sprite)
        
        Projectile(camera, at_pos, angle,  rand_speed, scale)
        Projectile(camera, at_pos, angle, rand_speed, scale, self.animtor.get_frame().image, SPRITE_TYPE_ASTEROID, dt)

    def spawn_rand_asteroid(self, camera, player, dt):
        player_pos = pygame.math.Vector2(player)
        spawnwidth , spawnheight = CENTER_SCREEN + 300, HEIGHT // 2 + 300
        rand_x = randint(player_pos.x - spawnwidth, player_pos.x + spawnwidth)
        rand_y = randint(player_pos.y - spawnheight, player_pos.y + spawnheight)
        rand_pos = pygame.math.Vector2(rand_x, rand_y)
        rand_scale = choice([1, 1, 1, 1.2])
        self.spawn_asteroid(camera, rand_scale, rand_pos, player, dt)