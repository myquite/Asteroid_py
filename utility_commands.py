import pygame
from constants import *
from star import Star
from goldorb import GoldOrb
from meteorite import Meteorite


class UtilityCommands:
    def __init__(self, game_objects):
        """
        Initialize utility commands with references to game objects
        game_objects should be a dict containing: player, asteroids, orbs, meteorites, stars, updatable, drawable
        """
        self.game_objects = game_objects
        self.enabled = False  # Toggle utility commands on/off (default: disabled)
        
    def handle_key_press(self, key):
        """Handle utility key commands"""
        # Always handle T key for toggle, regardless of enabled state
        if key == pygame.K_u:
            self.toggle_utility()
            return
            
        # Only handle other commands if enabled
        if not self.enabled:
            return
            
        if key == pygame.K_e:
            self.trigger_star_effect()
        elif key == pygame.K_g:
            self.spawn_gold_orb()
        elif key == pygame.K_m:
            self.spawn_meteorite()
        elif key == pygame.K_a:
            self.spawn_asteroid()
        elif key == pygame.K_p:
            self.add_points()
        elif key == pygame.K_c:
            self.clear_screen()
        elif key == pygame.K_1:
            self.spawn_gold_orb()
        elif key == pygame.K_2:
            self.spawn_meteorite()
        elif key == pygame.K_4:
            self.spawn_asteroid()
        elif key == pygame.K_5:
            self.add_points()
        elif key == pygame.K_6:
            self.clear_screen()
            
    def is_utility_mode_active(self):
        """Check if utility mode is currently active"""
        return self.enabled
            
    def trigger_star_effect(self):
        """E key - Trigger star explosion effect at player position"""
        print("UTILITY: Triggering star effect")
        player = self.game_objects['player']
        
        # Create a temporary star at player position
        temp_star = Star(player.position.x, player.position.y)
        
        # Vaporize all asteroids and collect their orbs
        exploded_asteroids = list(self.game_objects['asteroids'])
        total_orbs_created = 0
        
        for asteroid in exploded_asteroids:
            # Use the new method that drops orbs based on asteroid size
            new_orbs = asteroid.destroy_for_orbs()
            total_orbs_created += len(new_orbs)
            if new_orbs:
                for orb in new_orbs:
                    # Start the orb with blink animation
                    orb.start_blink_animation()
                    self.game_objects['orbs'].add(orb)
                    self.game_objects['updatable'].add(orb)
                    self.game_objects['drawable'].add(orb)
        
        # Start pull animation for ALL orbs (both existing and newly created)
        all_orbs = list(self.game_objects['orbs'])
        for orb in all_orbs:
            if orb.animation_state == 'normal':
                orb.start_pull_animation(player.position)
            elif orb.animation_state == 'blinking':
                # For blinking orbs, set the target but keep them blinking
                orb.set_pull_target(player.position)
            
        print(f"UTILITY: Destroyed {len(exploded_asteroids)} asteroids, created {total_orbs_created} orbs")
        
    def spawn_gold_orb(self):
        """G key or 1 key - Spawn a gold orb at player position"""
        print("UTILITY: Spawning gold orb")
        player = self.game_objects['player']
        orb = GoldOrb(player.position.x, player.position.y)
        self.game_objects['orbs'].add(orb)
        self.game_objects['updatable'].add(orb)
        self.game_objects['drawable'].add(orb)
        
    def spawn_meteorite(self):
        """M key or 2 key - Spawn a meteorite at player position"""
        print("UTILITY: Spawning meteorite")
        player = self.game_objects['player']
        meteorite = Meteorite(player.position.x, player.position.y)
        self.game_objects['meteorites'].add(meteorite)
        self.game_objects['updatable'].add(meteorite)
        self.game_objects['drawable'].add(meteorite)
        
    def spawn_asteroid(self):
        """A key or 4 key - Spawn an asteroid at player position"""
        print("UTILITY: Spawning asteroid")
        player = self.game_objects['player']
        from asteroid import Asteroid
        asteroid = Asteroid(player.position.x, player.position.y, ASTEROID_MIN_RADIUS * 2)
        self.game_objects['asteroids'].add(asteroid)
        self.game_objects['updatable'].add(asteroid)
        self.game_objects['drawable'].add(asteroid)
        
    def add_points(self):
        """P key or 5 key - Add 1000 points to player"""
        print("UTILITY: Adding 1000 points")
        player = self.game_objects['player']
        player.points += 1000
        print(f"UTILITY: Player score is now {player.points}")
        
    def clear_screen(self):
        """C key or 6 key - Clear all game objects except player"""
        print("UTILITY: Clearing screen")
        self.game_objects['asteroids'].empty()
        self.game_objects['orbs'].empty()
        self.game_objects['meteorites'].empty()
        self.game_objects['stars'].empty()
        print("UTILITY: Screen cleared")
        
    def toggle_utility(self):
        """T key - Toggle utility commands on/off"""
        self.enabled = not self.enabled
        status = "ENABLED" if self.enabled else "DISABLED"
        print(f"UTILITY: Commands {status}")
        
    def print_help(self):
        """Print available utility commands"""
        print("\n=== UTILITY COMMANDS ===")
        print("T - Toggle utility commands (currently DISABLED)")
        print("E - Trigger star explosion effect")
        print("G/1 - Spawn gold orb at player")
        print("M/2 - Spawn meteorite at player")
        print("A/4 - Spawn asteroid at player")
        print("P/5 - Add 1000 points")
        print("C/6 - Clear all objects")
        print("=======================\n") 