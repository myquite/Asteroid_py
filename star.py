import pygame
import random
from constants import *
from circleshape import CircleShape


class Star(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, STAR_RADIUS)
        # Add slight random velocity
        self.velocity = pygame.Vector2(
            random.uniform(-30, 30),
            random.uniform(-30, 30)
        )
        self.blink_timer = 0.0
        self.visible = True
        self.animation_state = 'normal'  # 'normal', 'blinking'

    def draw(self, screen):
        if not self.visible:
            return
            
        # Draw star as a bright yellow star shape
        points = []
        for i in range(5):
            angle = i * 72 - 90  # Start from top
            outer_point = pygame.Vector2(0, -self.radius).rotate(angle)
            inner_point = pygame.Vector2(0, -self.radius * 0.4).rotate(angle + 36)
            points.extend([self.position + outer_point, self.position + inner_point])
        
        pygame.draw.polygon(screen, (255, 255, 0), points)
        pygame.draw.polygon(screen, (255, 215, 0), points, 2)
        
        # Debug: Draw a small red dot to show star position
        pygame.draw.circle(screen, (255, 0, 0), self.position, 3)

    def update(self, dt):
        if self.animation_state == 'blinking':
            self.update_blink_animation(dt)
        else:
            # Apply friction
            self.velocity *= 0.98
            self.position += self.velocity * dt

    def update_blink_animation(self, dt):
        """Update blinking animation"""
        self.blink_timer += dt
        if self.blink_timer >= STAR_BLINK_RATE:
            self.visible = not self.visible
            self.blink_timer = 0.0

    def start_blink_animation(self):
        """Start the blinking animation"""
        self.animation_state = 'blinking'
        self.blink_timer = 0.0
        self.visible = True

    def is_collected_by(self, player):
        """Check if the star is close enough to be collected by the player"""
        return self.position.distance_to(player.position) <= STAR_COLLECTION_DISTANCE

    def explode_asteroids(self, asteroids):
        """Explode all asteroids within explosion radius"""
        exploded_asteroids = []
        for asteroid in asteroids:
            if self.position.distance_to(asteroid.position) <= STAR_EXPLOSION_RADIUS:
                exploded_asteroids.append(asteroid)
        return exploded_asteroids

    def absorb_orbs(self, orbs):
        """Absorb all orbs within explosion radius"""
        absorbed_orbs = []
        for orb in orbs:
            if self.position.distance_to(orb.position) <= STAR_EXPLOSION_RADIUS:
                absorbed_orbs.append(orb)
        return absorbed_orbs 