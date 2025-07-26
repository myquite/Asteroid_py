import sys
import pygame

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from goldorb import GoldOrb

def init_game():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    orbs = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    GoldOrb.containers = (orbs, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    return updatable, drawable, asteroids, shots, orbs, asteroid_field, player

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main(): 
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()  # Set the frame rate to 60 FPS
    dt = 0
    
    game_state = 'playing'  # or 'gameover'
    updatable, drawable, asteroids, shots, orbs, asteroid_field, player = init_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if game_state == 'gameover' and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    updatable, drawable, asteroids, shots, orbs, asteroid_field, player = init_game()
                    game_state = 'playing'

        if game_state == 'playing':
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_state = 'gameover'
                    break
                for shot in shots:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        # Get orbs from destroyed asteroid
                        new_orbs = asteroid.split()
                        if new_orbs:
                            for orb in new_orbs:
                                orbs.add(orb)
                                updatable.add(orb)
                                drawable.add(orb)

            # Check for orb collection
            for orb in orbs:
                if orb.is_collected_by(player):
                    player.collect_orb(orb)

        screen.fill((0, 0, 0))

        for obj in drawable:
            obj.draw(screen)

        # Display score
        draw_text(screen, f'Score: {player.points}', 36, (255, 255, 255), 100, 30)

        if game_state == 'gameover':
            draw_text(screen, 'GAME OVER', 100, (255, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            draw_text(screen, f'Final Score: {player.points}', 60, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            draw_text(screen, 'Press R to Restart', 50, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)

        pygame.display.flip()

        dt = clock.tick(60) /1000  # Convert milliseconds to seconds


if __name__ == "__main__":
    main()
