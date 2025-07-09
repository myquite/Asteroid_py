import pygame

from constants import *

def main(): 
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()  # Set the frame rate to 60 FPS
    dt = 0
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
        screen.fill((0, 0, 0))
        pygame.display.flip()

        dt = clock.tick(60) /1000  # Convert milliseconds to seconds



if __name__ == "__main__":
    main()
