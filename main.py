import asyncio
import pygame

from src.constants.colors import lightblue
import src.constants as constants
import src.components as components
# import src.game as game

running = True

camera = components.CameraNew()

player = {"centerx": 0, "centery": 0}
clock = pygame.time.Clock()
delta_time = 0.0

async def main():
    global running, player, delta_time
    pygame.init()
    pygame.display.set_caption("Astro!")
    screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))

    camera.on_start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player["centerx"] += 500 * delta_time
        player["centery"] += 500 * delta_time
        camera.center_target(player["centerx"], player["centery"])

        screen.fill(lightblue)

        camera.draw(screen)
        pygame.display.update()
        delta_time = clock.tick(60) / 1000.0
        await asyncio.sleep(0)


if __name__ == "__main__":
    # astro = game.Game()
    # astro.run()
    asyncio.run(main())
