import sys
import pygame

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from goldorb import GoldOrb
from highscore import HighScore

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
    
    game_state = 'countdown'  # 'countdown', 'playing', 'gameover', 'highscore_input'
    countdown_timer = 0.0
    countdown_phase = 'prepare'  # 'prepare' or 'countdown'
    
    updatable, drawable, asteroids, shots, orbs, asteroid_field, player = init_game()
    high_score_manager = HighScore()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if game_state == 'gameover' and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    updatable, drawable, asteroids, shots, orbs, asteroid_field, player = init_game()
                    game_state = 'countdown'
                    countdown_timer = 0.0
                    countdown_phase = 'prepare'

        if game_state == 'countdown':
            countdown_timer += dt
            
            if countdown_phase == 'prepare':
                if countdown_timer >= PREPARE_DISPLAY_TIME:
                    countdown_phase = 'countdown'
                    countdown_timer = 0.0
            elif countdown_phase == 'countdown':
                if countdown_timer >= COUNTDOWN_DURATION:
                    game_state = 'playing'
                    countdown_timer = 0.0

        elif game_state == 'playing':
            updatable.update(dt)

            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_state = 'gameover'
                    # Check if this is a high score
                    if high_score_manager.is_high_score(player.points):
                        game_state = 'highscore_input'
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

        elif game_state == 'highscore_input':
            # Get player name for high score
            player_name = high_score_manager.get_name_input(screen, player.points)
            if player_name:
                high_score_manager.add_score(player_name, player.points)
            game_state = 'gameover'

        screen.fill((0, 0, 0))

        # Draw game objects during countdown and playing states
        if game_state in ['countdown', 'playing']:
            for obj in drawable:
                obj.draw(screen)

        # Draw countdown screen
        if game_state == 'countdown':
            if countdown_phase == 'prepare':
                draw_text(screen, 'BE PREPARED', 72, (255, 215, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            elif countdown_phase == 'countdown':
                remaining_time = COUNTDOWN_DURATION - countdown_timer
                countdown_number = int(remaining_time) + 1
                if countdown_number > 0:
                    draw_text(screen, str(countdown_number), 120, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

        # Display current score during gameplay
        if game_state == 'playing':
            draw_text(screen, f'Score: {player.points}', 36, (255, 255, 255), 100, 30)
            # Display high scores during gameplay
            high_score_manager.draw_high_scores(screen, SCREEN_WIDTH - 200, 30)

        if game_state == 'gameover':
            draw_text(screen, 'GAME OVER', 100, (255, 0, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
            draw_text(screen, f'Final Score: {player.points}', 60, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20)
            
            # Show if it's a high score
            if high_score_manager.is_high_score(player.points):
                draw_text(screen, 'NEW HIGH SCORE!', 48, (255, 215, 0), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            
            # Display high scores
            high_score_manager.draw_high_scores(screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 80)
            
            draw_text(screen, 'Press R to Restart', 50, (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

        pygame.display.flip()

        dt = clock.tick(60) /1000  # Convert milliseconds to seconds


if __name__ == "__main__":
    main()
