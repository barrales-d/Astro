import pygame
from colors import *
from settings import *
from player import Player
from projectile import Projectile
from camera import Camera
from random import randint, choice
import math

# game setup
class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Astro')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('./font/Pixeltype.ttf', 60)
        self.running = True
        self.game_active = False
        self.delta_time = 0
        self.reset()

        self.bg_music = pygame.mixer.Sound('./music/wonderful_transportation_sega_genesis.mp3')
        self.bg_music.set_volume(0.1)
        self.bg_music.play(-1)

        self.player_death = pygame.mixer.Sound('./music/deathsound.ogg')
        self.asteroid_death = self.player_death
        self.asteroid_death.set_volume(0.5)
        self.lazer_sound = pygame.mixer.Sound('./music/laserpew.ogg')

        self.asteroid_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.asteroid_timer, 1000) 

    def reset(self):
        self.score = 0

        self.camera = Camera(self.screen)
        self.camera.empty()
        
        self.player = Player((WIDTH // 2, HEIGHT // 2), self.camera)

    def display_text(self, pos, text):
        text_surface = self.font.render(text, False, white)
        text_rect = text_surface.get_rect(center = pos)
        self.screen.blit(text_surface, text_rect)

    def spawn_asteroid(self, scale, at_pos):
        at_pos = pygame.math.Vector2(at_pos)
        player_pos = pygame.math.Vector2(self.player.rect.center)
        angle = math.atan2(at_pos.y - player_pos.y , at_pos.x - player_pos.x)
        rand_speed = randint(100, 300)
        Projectile(self.camera, scale, angle, at_pos, self.delta_time, rand_speed, SPRITE_TYPE_ASTEROID)
    
    def spawn_rand_asteroid(self):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        spawnwidth , spawnheight = WIDTH // 2 + 300, HEIGHT // 2 + 300 
        player_pad = self.player.rect.size[0]
        rand_x = randint(player_pos.x - spawnwidth + player_pad, player_pos.x + spawnwidth + player_pad)
        rand_y = randint(player_pos.y - spawnheight + player_pad, player_pos.y + spawnheight + player_pad)
        rand_pos = pygame.math.Vector2(rand_x, rand_y)
        rand_scale = choice([1, 1, 1, 1.2])
        self.spawn_asteroid(rand_scale, rand_pos)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.game_active:
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_j or event.key == pygame.K_z):
                    Projectile(self.camera, 2.3, self.player.angle, self.player.rect.center, self.delta_time, 800, SPRITE_TYPE_BULLET)
                    self.lazer_sound.play(0, 0, 200)

                if event.type == self.asteroid_timer:
                    self.spawn_rand_asteroid()    
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.game_active = True
    
    def asteroid_collision(self):
        asteroids = self.camera.get_asteroids()
        if self.player.rect.collidelist(asteroids) < 0:
            return True
        
        self.player_death.play(0, 0, 500)
        return False
    
    def bullet_collsion(self):
        asteroids = self.camera.get_asteroids()
        bullets = self.camera.get_bullets()
        for asteroid in asteroids:
            bullet_idx = asteroid.rect.collidelist(bullets)
            if bullet_idx > 0:
                bullets[bullet_idx].kill()
                self.asteroid_death.play(0, 100, 0)
                plus_score = int(10 *  (1 / asteroid.scale))
                self.score += plus_score
                self.display_text(asteroid.rect.topleft - self.camera.offset, '+'+ str(plus_score))

                if asteroid.scale > 0.9:
                    # spawn two asteroids
                    if choice([0, 0, 1]) == 0:
                        self.spawn_asteroid(asteroid.scale * 0.9, asteroid.rect.center)
                        self.spawn_asteroid(asteroid.scale * 0.9, asteroid.rect.center)
                    else:
                        self.spawn_asteroid(asteroid.scale * 0.9, asteroid.rect.center)
                
                asteroid.kill() # this works! it deletes the object in self.camera.sprites()
    
    def run(self):
        while self.running:
            self.handle_events()
            if self.game_active:
                self.screen.fill(black)

                self.camera.update()
                bg_boundary = self.camera.background.get_bounding_rect()
                self.player.rect.clamp_ip(bg_boundary)
                self.camera.draw_sprites(self.player.rect)
                self.display_text((WIDTH // 2, HEIGHT // 6), f'Score: {self.score}')
                
                self.game_active = self.asteroid_collision()
                self.bullet_collsion()
            else:
                self.screen.blit(self.camera.background, self.camera.background_rect)
                self.display_text((WIDTH // 2, HEIGHT // 6), 'ASTRO!!')
                self.display_text((WIDTH // 2, HEIGHT // 4), '[W ARROW] to move forward,')
                self.display_text((WIDTH // 2, HEIGHT // 4 + 50), '[A/D] to rotate left/right')
                self.display_text((WIDTH // 2, HEIGHT // 4 + 100), 'J to fire lazer')
                self.display_text((WIDTH // 2, HEIGHT * 4 // 5), 'Press space to start!')
                self.screen.blit(self.player.unrotated_image, self.player.unrotated_rect)
                self.reset()

            pygame.display.update()
            self.delta_time = self.clock.tick(60) / 1000
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()