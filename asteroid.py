import pygame
import random
from constants import *
from circleshape import CircleShape


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        """Split the asteroid and return gold orbs if it's a small asteroid"""
        orbs_to_spawn = []
        
        # If this is a small asteroid (minimum size), drop a gold orb
        if self.radius <= ASTEROID_MIN_RADIUS:
            from goldorb import GoldOrb
            orb = GoldOrb(self.position.x, self.position.y)
            orbs_to_spawn.append(orb)
            self.kill()
            return orbs_to_spawn

        self.kill()

        # randomize the angle of the split
        random_angle = random.uniform(20, 50)

        a = self.velocity.rotate(random_angle)
        b = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = a * 1.2
        asteroid = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid.velocity = b * 1.2
        
        return orbs_to_spawn