import pygame
from colors import *
from settings import *
from player import Player
from buttons import *
from projectile import *
from camera import Camera
from random import randint, choice
import math

def display_text(screen, font, pos, text):
        text_surface = font.render(text, False, white)
        text_rect = text_surface.get_rect(center = pos)
        screen.blit(text_surface, text_rect)
# game setup
class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Astro')
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font('./font/Pixeltype.ttf', 80)
        self.title_font.set_bold(True)
        self.font60 = pygame.font.Font('./font/Pixeltype.ttf', 60)
        self.font30 = pygame.font.Font('./font/Pixeltype.ttf', 30)
        self.projectile_lazer = ProjectileKind(SPRITE_TYPE_BULLET, pygame.image.load('./graphics/lazer.png'), 2.3)
        self.projectile_asteroid = ProjectileKind(SPRITE_TYPE_ASTEROID, pygame.image.load('./graphics/asteroid.png'), 1)
        self.running = True
        self.game_active = False
        self.state = STATE_MENU
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
        self.player = Player((randint(100, self.camera.background.get_width()), randint(100, self.camera.background.get_height())), self.camera)

    def spawn_asteroid(self, scale, at_pos):
        at_pos = pygame.math.Vector2(at_pos)
        player_pos = pygame.math.Vector2(self.player.rect.center)
        angle = math.atan2(at_pos.y - player_pos.y , at_pos.x - player_pos.x)
        rand_speed = randint(100, 300)
        self.projectile_asteroid.scale = scale
        Projectile(self.camera, at_pos, angle,  rand_speed, self.projectile_asteroid, self.delta_time)
    
    def spawn_rand_asteroid(self):
        player_pos = pygame.math.Vector2(self.player.rect.center)
        spawnwidth , spawnheight = CENTER_SCREEN + 300, HEIGHT // 2 + 300 
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

            if self.state == STATE_PLAY:
                if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_j):
                    Projectile(self.camera, self.player.rect.center, self.player.angle, 800, self.projectile_lazer, self.delta_time)
                    self.lazer_sound.play(0, 0, 200)

                if event.type == self.asteroid_timer:
                    self.spawn_rand_asteroid()

    def handle_asteroid_collision(self):
        asteroids = self.camera.get_asteroids()
        if self.player.rect.collidelist(asteroids) < 0:
            return True
        
        self.player_death.play(0, 0, 500)
        return False
    
    def handle_bullet_collsion(self):
        asteroids = self.camera.get_asteroids()
        bullets = self.camera.get_bullets()
        for asteroid in asteroids:
            bullet_idx = asteroid.rect.collidelist(bullets)
            if bullet_idx > 0:
                bullets[bullet_idx].kill()
                self.asteroid_death.play(0, 100, 0)
                plus_score = int(10 *  (1 / asteroid.kind.scale))
                self.score += plus_score
                display_text(self.screen, self.font60, asteroid.rect.topleft - self.camera.offset, '+'+ str(plus_score))

                if asteroid.kind.scale > 0.9:
                    # spawn two asteroids
                    if choice([0, 0, 1]) == 0:
                        self.spawn_asteroid(asteroid.kind.scale * 0.9, asteroid.rect.center)
                        self.spawn_asteroid(asteroid.kind.scale * 0.9, asteroid.rect.center)
                    else:
                        self.spawn_asteroid(asteroid.kind.scale * 0.9, asteroid.rect.center)
                
                asteroid.kill() # this works! it deletes the object in self.camera.sprites()
    
    def render_titlescreen(self):
        title_pos = (CENTER_SCREEN, HEIGHT // 6)
        btn_center_x = title_pos[0] - BTN_WIDTH // 2
        btn_center_y = title_pos[1] + BTN_HEIGHT

        display_text(self.screen, self.title_font, title_pos, 'A    S    T    R    O')
        self.player.unrotated_rect.center = (CENTER_SCREEN, btn_center_y + BTN_PAD * 4)
        btn_center_y += self.player.unrotated_rect.h + BTN_PAD
        if(createButton(self.screen, self.font30, btn_center_x, btn_center_y, BTN_WIDTH, BTN_HEIGHT, 'Start')):
            self.state = STATE_PLAY
        btn_center_y += BTN_HEIGHT + BTN_PAD
        if(createButton(self.screen, self.font30, btn_center_x, btn_center_y, BTN_WIDTH, BTN_HEIGHT, 'Controls')):
            self.state = STATE_CONTROLS
        btn_center_y += BTN_HEIGHT + BTN_PAD
        if(createButton(self.screen, self.font30, btn_center_x, btn_center_y, BTN_WIDTH, BTN_HEIGHT, 'Quit')):
            self.running = False
        btn_center_y += BTN_HEIGHT + BTN_PAD
        self.screen.blit(self.player.unrotated_image, self.player.unrotated_rect)


    def render_gameplay(self):
        self.screen.fill(black)

        self.camera.update()
        bg_boundary = self.camera.background.get_bounding_rect()
        self.player.rect.clamp_ip(bg_boundary)
        self.camera.draw_sprites(self.player.rect)
        display_text(self.screen, self.font60, (CENTER_SCREEN, HEIGHT // 6), f'Score: {self.score}')
        
        # self.game_active = self.handle_asteroid_collision()
        if not self.handle_asteroid_collision():
            self.state = STATE_DEATH
        self.handle_bullet_collsion()
    
    def render_death_screen(self):
        pygame.time.delay(2000)
        self.state = STATE_MENU

    def render_controls(self):
        UI_height = HEIGHT // 8
        if(createButton(self.screen, self.font30, CENTER_SCREEN // 6, UI_height, BTN_WIDTH, BTN_HEIGHT, 'Back')):
            self.state = STATE_MENU
        UI_height = HEIGHT // 3
        display_text(self.screen, self.font60, (CENTER_SCREEN, UI_height), '[W ARROW] to move forward, [SHIFT] to boost')
        UI_height += BTN_HEIGHT + BTN_PAD
        display_text(self.screen, self.font60, (CENTER_SCREEN, UI_height), '[A/D] to rotate left/right')
        UI_height += BTN_HEIGHT + BTN_PAD
        display_text(self.screen, self.font60, (CENTER_SCREEN, UI_height), '[J] to fire lazer')

    def run(self):
        while self.running:
            self.handle_events()
            self.screen.blit(self.camera.background, self.camera.background_rect)
            if self.state == STATE_MENU:
                self.render_titlescreen()
            elif self.state == STATE_PLAY:
                self.render_gameplay()
            elif self.state == STATE_DEATH:
                self.render_death_screen()
            elif self.state == STATE_CONTROLS:
                self.render_controls()
            else: 
                # UNREACHABLE
                self.running = False
            pygame.display.update()
            self.delta_time = self.clock.tick(60) / 1000
        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()