import pygame
import random
from constants import *
from circleshape import CircleShape


class Meteorite(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, METEORITE_RADIUS)
        # Set a random direction and speed
        angle = random.uniform(0, 360)
        self.velocity = pygame.Vector2(0, 1).rotate(angle) * METEORITE_SPEED

    def draw(self, screen):
        # Draw meteorite as a dark gray circle with a trail effect
        pygame.draw.circle(screen, (64, 64, 64), self.position, self.radius)
        pygame.draw.circle(screen, (128, 128, 128), self.position, self.radius - 3)

    def update(self, dt):
        self.position += self.velocity * dt
        
        # Remove if off screen
        if (self.position.x < -METEORITE_RADIUS or 
            self.position.x > SCREEN_WIDTH + METEORITE_RADIUS or
            self.position.y < -METEORITE_RADIUS or 
            self.position.y > SCREEN_HEIGHT + METEORITE_RADIUS):
            self.kill()

    def destroy(self):
        """Called when meteorite is destroyed, returns a blinking star"""
        from star import Star
        star = Star(self.position.x, self.position.y)
        # Make the star start blinking
        star.start_blink_animation()
        self.kill()
        return star 