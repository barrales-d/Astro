import pygame
import math
from random import randint, choice

from ..constants.settings import (
    SPRITE_COLOR_KEY,
    SPRITE_TYPE_ASTEROID,
    SPRITE_SCALER,
    CENTER_SCREEN,
    HEIGHT,
    SPRITE_TYPE_BULLET,
)
from ..components.animator import Animator


PROJECTILE_DESPAWN_TIMER = 10


class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, pos, angle, speed, sprite, scale, kind, dt):
        super().__init__(group)
        self.angle = angle
        self.type = kind
        self.scale = scale
        self.unrotated_image = pygame.transform.scale_by(sprite, self.scale)

        self.unrotated_rect = self.unrotated_image.get_rect(center=pos)
        self.image = self.unrotated_image
        self.rect = self.image.get_rect(center=pos)
        self.rotate_image()

        self.speed = speed
        self.dx = math.sin(self.angle) * self.speed * dt
        self.dy = math.cos(self.angle) * self.speed * dt
        self.dt = dt

        self.despawn_timer = PROJECTILE_DESPAWN_TIMER

    def rotate_image(self):
        self.image = pygame.transform.rotate(
            self.unrotated_image, self.angle * 180 / math.pi
        )
        self.image.convert_alpha()
        # self.image.set_colorkey(SPRITE_COLOR_KEY)
        self.rect.centerx = self.unrotated_rect.centerx - (self.image.get_width() // 2)
        self.rect.centery = self.unrotated_rect.centery - (self.image.get_height() // 2)
        self.mask = pygame.mask.from_surface(self.image)

    def destroy(self):
        if self.despawn_timer > 0:
            self.despawn_timer -= self.dt
        else:
            self.kill()

    def update(self):
        self.unrotated_rect.x += self.dx
        self.unrotated_rect.y += self.dy

        if self.type == SPRITE_TYPE_ASTEROID:
            self.angle += self.dt * self.dt * self.speed
            self.angle %= 2 * math.pi
            self.rotate_image()
        else:
            self.rect.x = self.unrotated_rect.x
            self.rect.y = self.unrotated_rect.y

        self.destroy()


class ProjectileManager:
    def __init__(self):
        self.__animtor = Animator(
            "./graphics/asteroid_spritesheet_outline.png", 32, 1, 3, (0, 0)
        )

        self.__animtor.add("asteroid1", 1, 1, 1)
        self.__animtor.add("asteroid2", 1, 2, 2)
        self.__animtor.add("asteroid3", 1, 3, 3)

        self.__lazer_sprite = pygame.image.load("./graphics/lazer.png").convert_alpha()

    def spawn_asteroid(self, camera, scale, a_pos, player, dt):
        at_pos = pygame.math.Vector2(a_pos)
        player_pos = pygame.math.Vector2(player)
        angle = math.atan2(at_pos.y - player_pos.y, at_pos.x - player_pos.x)
        rand_speed = randint(100, 300)
        if scale > SPRITE_SCALER:
            rand_speed = randint(80, 150)
        rand_sprite = choice(["asteroid1", "asteroid2", "asteroid3"])
        self.__animtor.play(rand_sprite)

        Projectile(
            camera,
            at_pos,
            angle,
            rand_speed,
            self.__animtor.get_frame().image,
            scale,
            SPRITE_TYPE_ASTEROID,
            dt,
        )

    def spawn_rand_asteroid(self, camera, player, dt):
        player_pos = pygame.math.Vector2(player)
        spawnwidth, spawnheight = CENTER_SCREEN + 300, HEIGHT // 2 + 300
        rand_x = randint(int(player_pos.x - spawnwidth), int(player_pos.x + spawnwidth))
        rand_y = randint(
            int(player_pos.y - spawnheight), int(player_pos.y + spawnheight)
        )
        rand_pos = pygame.math.Vector2(rand_x, rand_y)
        rand_scale = choice(
            [SPRITE_SCALER, SPRITE_SCALER, SPRITE_SCALER, SPRITE_SCALER * 1.5]
        )
        self.spawn_asteroid(camera, rand_scale, rand_pos, player, dt)

    def spawn_lazer(self, camera, player_pos, angle, speed, dt):
        Projectile(
            camera,
            player_pos,
            angle,
            speed,
            self.__lazer_sprite,
            SPRITE_SCALER,
            SPRITE_TYPE_BULLET,
            dt,
        )
