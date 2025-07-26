import sys
import pygame

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from goldorb import GoldOrb
from meteorite import Meteorite
from star import Star
from highscore import HighScore

def init_game():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    orbs = pygame.sprite.Group()
    meteorites = pygame.sprite.Group()
    stars = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    GoldOrb.containers = (orbs, updatable, drawable)
    Meteorite.containers = (meteorites, updatable, drawable)
    Star.containers = (stars, updatable, drawable)
    AsteroidField.containers = updatable
    asteroid_field = AsteroidField()
    Player.containers = (updatable, drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    return updatable, drawable, asteroids, shots, orbs, meteorites, stars, asteroid_field, player

def draw_text(screen, text, size, color, x, y):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def spawn_meteorite():
    """Spawn a meteorite from a random edge"""
    import random
    edge = random.choice(['top', 'bottom', 'left', 'right'])
    
    if edge == 'top':
        x = random.randint(0, SCREEN_WIDTH)
        y = -METEORITE_RADIUS
    elif edge == 'bottom':
        x = random.randint(0, SCREEN_WIDTH)
        y = SCREEN_HEIGHT + METEORITE_RADIUS
    elif edge == 'left':
        x = -METEORITE_RADIUS
        y = random.randint(0, SCREEN_HEIGHT)
    else:  # right
        x = SCREEN_WIDTH + METEORITE_RADIUS
        y = random.randint(0, SCREEN_HEIGHT)
    
    return Meteorite(x, y)

def main(): 
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()  # Set the frame rate to 60 FPS
    dt = 0
    
    game_state = 'countdown'  # 'countdown', 'playing', 'gameover', 'highscore_input'
    countdown_timer = 0.0
    countdown_phase = 'prepare'  # 'prepare' or 'countdown'
    meteorite_spawn_timer = 0.0
    explosion_timer = 0.0
    explosion_position = None
    white_flash_timer = 0.0
    
    updatable, drawable, asteroids, shots, orbs, meteorites, stars, asteroid_field, player = init_game()
    high_score_manager = HighScore()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if game_state == 'gameover' and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Restart the game
                    updatable, drawable, asteroids, shots, orbs, meteorites, stars, asteroid_field, player = init_game()
                    game_state = 'countdown'
                    countdown_timer = 0.0
                    countdown_phase = 'prepare'
                    meteorite_spawn_timer = 0.0
                    explosion_timer = 0.0
                    explosion_position = None
                    white_flash_timer = 0.0

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
            
            # Update explosion effect
            if explosion_timer > 0:
                explosion_timer -= dt
            
            # Update white flash effect
            if white_flash_timer > 0:
                white_flash_timer -= dt
            
            # Spawn meteorites
            meteorite_spawn_timer += dt
            if meteorite_spawn_timer >= METEORITE_SPAWN_RATE:
                meteorite_spawn_timer = 0.0
                new_meteorite = spawn_meteorite()
                meteorites.add(new_meteorite)
                updatable.add(new_meteorite)
                drawable.add(new_meteorite)

            # Check player collision with asteroids
            for asteroid in asteroids:
                if asteroid.collides_with(player):
                    game_state = 'gameover'
                    # Check if this is a high score
                    if high_score_manager.is_high_score(player.points):
                        game_state = 'highscore_input'
                    break

            # Check shot collisions with asteroids
            for shot in shots:
                for asteroid in asteroids:
                    if asteroid.collides_with(shot):
                        shot.kill()
                        # Get orbs from destroyed asteroid
                        new_orbs = asteroid.split()
                        if new_orbs:
                            for orb in new_orbs:
                                orbs.add(orb)
                                updatable.add(orb)
                                drawable.add(orb)

            # Check shot collisions with meteorites
            for shot in shots:
                for meteorite in meteorites:
                    if meteorite.collides_with(shot):
                        shot.kill()
                        # Create star from destroyed meteorite
                        new_star = meteorite.destroy()
                        stars.add(new_star)
                        updatable.add(new_star)
                        drawable.add(new_star)

            # Check for orb collection
            for orb in orbs:
                if orb.is_collected_by(player):
                    player.collect_orb(orb)

            # Check for star collection
            for star in stars:
                if star.is_collected_by(player):
                    # Store star position before killing it
                    star_position = star.position.copy()
                    player.collect_star(star)
                    # Use star power immediately
                    player.use_star_power()
                    
                    # Start explosion effect
                    explosion_timer = STAR_EXPLOSION_DURATION
                    explosion_position = star_position
                    
                    # Start white flash effect
                    white_flash_timer = STAR_WHITE_FLASH_DURATION
                    
                    # VAPORIZE ALL asteroids on screen (no distance check needed)
                    exploded_asteroids = list(asteroids)  # Convert to list to avoid modification during iteration
                    
                    for asteroid in exploded_asteroids:
                        # Create orbs from exploded asteroids
                        new_orbs = asteroid.split()
                        if new_orbs:
                            for orb in new_orbs:
                                orbs.add(orb)
                                updatable.add(orb)
                                drawable.add(orb)
                    
                    # ABSORB ALL orbs on screen (no distance check needed)
                    absorbed_orbs = list(orbs)  # Convert to list to avoid modification during iteration
                    
                    for orb in absorbed_orbs:
                        player.collect_orb(orb)

        elif game_state == 'highscore_input':
            # Get player name for high score
            player_name = high_score_manager.get_name_input(screen, player.points)
            if player_name:
                high_score_manager.add_score(player_name, player.points)
            game_state = 'gameover'

        # Draw white flash effect first (if active)
        if white_flash_timer > 0:
            # Calculate flash intensity (fade from white to transparent)
            flash_alpha = int((white_flash_timer / STAR_WHITE_FLASH_DURATION) * 255)
            flash_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            flash_surface.fill((255, 255, 255))
            flash_surface.set_alpha(flash_alpha)
            screen.blit(flash_surface, (0, 0))
        else:
            screen.fill((0, 0, 0))

        # Draw game objects during countdown and playing states
        if game_state in ['countdown', 'playing']:
            for obj in drawable:
                obj.draw(screen)

        # Draw explosion effect (only if not in white flash)
        if explosion_timer > 0 and explosion_position and white_flash_timer <= 0:
            alpha = int((explosion_timer / STAR_EXPLOSION_DURATION) * 255)
            # Create a surface for the explosion effect
            explosion_surface = pygame.Surface((STAR_EXPLOSION_RADIUS * 2, STAR_EXPLOSION_RADIUS * 2), pygame.SRCALPHA)
            pygame.draw.circle(explosion_surface, (255, 255, 0, alpha), (STAR_EXPLOSION_RADIUS, STAR_EXPLOSION_RADIUS), STAR_EXPLOSION_RADIUS)
            screen.blit(explosion_surface, (explosion_position.x - STAR_EXPLOSION_RADIUS, explosion_position.y - STAR_EXPLOSION_RADIUS))

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
