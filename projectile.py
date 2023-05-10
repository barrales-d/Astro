import pygame
import math
from settings import *
from colors import *

PROJECTILE_DESPAWN_TIMER = 10

class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, scale, angle, pos, dt, speed, type):
        super().__init__(group)
        self.type = type
        self.angle = angle
        self.scale = scale
        if self.type == SPRITE_TYPE_ASTROID:
            self.unrotated_image = pygame.transform.scale_by(pygame.image.load('./graphics/astroid.png').convert_alpha(), self.scale)
        elif self.type == SPRITE_TYPE_BULLET:
            self.unrotated_image = pygame.transform.scale_by(pygame.image.load('./graphics/lazer.png').convert_alpha(), self.scale)
        
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

        if self.type == SPRITE_TYPE_ASTROID:
            self.angle += self.dt * self.dt *  self.speed
            self.angle %= (2 * math.pi)
            self.rotate_image()
        else:
            self.rect.x = self.unrotated_rect.x
            self.rect.y = self.unrotated_rect.y

        self.destroy()