import pygame

from constants import *
from player import Player

def main(): 
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()  # Set the frame rate to 60 FPS
    dt = 0

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        player.update(dt)

        screen.fill((0, 0, 0))
        player.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60) /1000  # Convert milliseconds to seconds

       


if __name__ == "__main__":
    main()
