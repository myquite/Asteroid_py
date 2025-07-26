import pygame
import random
from constants import *
from circleshape import CircleShape


class GoldOrb(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, GOLD_ORB_RADIUS)
        # Add a slight random velocity to make orbs drift
        self.velocity = pygame.Vector2(
            random.uniform(-20, 20),
            random.uniform(-20, 20)
        )
        # Animation states
        self.animation_state = 'normal'  # 'normal', 'blinking', 'pulling'
        self.animation_timer = 0.0
        self.original_position = pygame.Vector2(x, y)
        self.target_position = None
        self.visible = True
        self.scored = False  # Track if points have been awarded for this orb

    def draw(self, screen):
        if not self.visible:
            return
            
        # Draw a golden circle with a slight glow effect
        pygame.draw.circle(screen, (255, 215, 0), self.position, self.radius)
        pygame.draw.circle(screen, (255, 255, 0), self.position, self.radius - 2)

    def update(self, dt):
        if self.animation_state == 'blinking':
            self.update_blink_animation(dt)
        elif self.animation_state == 'pulling':
            self.update_pull_animation(dt)
        else:
            # Normal behavior
            self.velocity *= 0.98
            self.position += self.velocity * dt

    def update_blink_animation(self, dt):
        """Update blinking into existence animation"""
        self.animation_timer += dt
        progress = self.animation_timer / ORB_BLINK_DURATION
        
        if progress >= 1.0:
            # Blinking complete, start pulling to player
            self.animation_state = 'pulling'
            self.animation_timer = 0.0
            self.visible = True
            # Note: target_position will be set by the main game loop
        else:
            # Blink effect - fade in
            self.visible = progress > 0.5

    def update_pull_animation(self, dt):
        """Update pulling to player animation"""
        if not self.target_position:
            # If no target set, just stay in place
            return
            
        self.animation_timer += dt
        progress = self.animation_timer / ORB_PULL_DURATION
        
        if progress >= 1.0:
            # Pulling complete, orb is collected
            self.kill()
        else:
            # Smooth movement towards target
            self.position = self.original_position.lerp(self.target_position, progress)

    def start_blink_animation(self):
        """Start the blink into existence animation"""
        self.animation_state = 'blinking'
        self.animation_timer = 0.0
        self.visible = False

    def start_pull_animation(self, target_position):
        """Start the pull to player animation"""
        self.animation_state = 'pulling'
        self.animation_timer = 0.0
        self.original_position = self.position.copy()
        self.target_position = target_position
        self.visible = True

    def set_pull_target(self, target_position):
        """Set the target position for pulling (used when blinking completes)"""
        self.target_position = target_position
        self.original_position = self.position.copy()

    def is_collected_by(self, player):
        """Check if the orb is close enough to be collected by the player"""
        return self.position.distance_to(player.position) <= GOLD_ORB_COLLECTION_DISTANCE 