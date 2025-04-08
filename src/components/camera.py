import pygame
from ..constants.settings import SPRITE_TYPE_ASTEROID, SPRITE_TYPE_BULLET


class Camera(pygame.sprite.Group):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        wd, ht = self.screen.get_size()
        self.h_width = wd / 2
        self.h_height = ht / 2
        self.offset = pygame.math.Vector2()
        self.background = pygame.image.load(
            "./graphics/asteroid_background.png"
        ).convert_alpha()
        self.background_rect = self.background.get_rect(topleft=(0, 0))

    def get_asteroids(self):
        return [
            sprite for sprite in self.sprites() if sprite.type == SPRITE_TYPE_ASTEROID
        ]

    def get_bullets(self):
        return [
            sprite for sprite in self.sprites() if sprite.type == SPRITE_TYPE_BULLET
        ]

    def center_target(self, target):
        self.offset.x = target.centerx - self.h_width
        self.offset.y = target.centery - self.h_height

    def draw_sprites(self, player_rect):
        self.center_target(player_rect)

        bg_offset = self.background_rect.topleft - self.offset
        self.screen.blit(self.background, bg_offset)

        sprites = self.sprites()
        for sprite_idx in range(1, len(sprites)):
            sprite = sprites[sprite_idx]
            offset_pos = sprite.rect.topleft - self.offset
            self.screen.blit(sprite.image, offset_pos)

        self.screen.blit(sprites[0].image, sprites[0].rect.topleft - self.offset)
