import pygame
import math
from colors import *
from settings import *


MAX_DRIFT_TIMER = 5
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.type = SPRITE_TYPE_PLAYER
        self.angle = 0
        self.prev_angle = self.angle
        self.float = pygame.transform.scale_by(pygame.image.load('./graphics/ship/float.png').convert_alpha(), 4)
        self.shoot = pygame.transform.scale_by(pygame.image.load('./graphics/ship/shoot.png').convert_alpha(), 4)
        self.boost = pygame.transform.scale_by(pygame.image.load('./graphics/ship/boost2.png').convert_alpha(), 4)
        self.boost1 = pygame.transform.scale_by(pygame.image.load('./graphics/ship/boost1.png').convert_alpha(), 4)
        self.animation = [self.boost, self.boost1]
        self.boost_index = 0

        self.unrotated_image =  self.float
        self.unrotated_rect = self.unrotated_image.get_rect(center = pos)
        self.image = self.unrotated_image
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect(center = pos)
        self.rotate_image()

        self.speed = pygame.math.Vector2(500, 500)
        self.rotation_speed = 5
        self.drift_timer = 0

    def rotate_image(self):
        self.image = pygame.transform.rotate(self.unrotated_image, self.angle * 180 / math.pi)
        self.image.set_colorkey(black)
        self.rect.centerx = self.unrotated_rect.centerx - (self.image.get_width() // 2)
        self.rect.centery = self.unrotated_rect.centery - (self.image.get_height() // 2)

    def update(self):
        dt = 0.016
        keys = pygame.key.get_pressed()
        
        if self.drift_timer >= 0:
            self.drift_timer -= dt

        def abs(x): 
            if x < 0: return -x
            else: return x
                
        t = abs(self.drift_timer / MAX_DRIFT_TIMER)
        drift_x_speed = (math.sin(self.prev_angle) * 50 * dt)
        drift_y_speed = (math.cos(self.prev_angle) * 50 * dt)

        dx = pygame.math.lerp(0, drift_x_speed, t)
        dy = pygame.math.lerp(0, drift_y_speed, t)

        self.unrotated_image =  self.float
        if keys[pygame.K_j]:
            self.unrotated_image =  self.shoot
        
        speed_boost = 1
        if keys[pygame.K_SPACE]:
            speed_boost = 1.5

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.boost_index = (self.boost_index + 0.1) % len(self.animation)
            self.unrotated_image =  self.animation[int(self.boost_index)]
             
            dx = (math.sin(self.angle) * self.speed.x) * dt * speed_boost
            dy = (math.cos(self.angle) * self.speed.y) * dt * speed_boost
            self.prev_angle = self.angle
            self.drift_timer = MAX_DRIFT_TIMER

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.angle += dt * self.rotation_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.angle -= dt * self.rotation_speed
        self.angle %= (2 * math.pi)

        self.unrotated_rect.x += dx
        self.unrotated_rect.y += dy
        self.rotate_image()