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

    def draw(self, screen):
        # Draw a golden circle with a slight glow effect
        pygame.draw.circle(screen, (255, 215, 0), self.position, self.radius)
        pygame.draw.circle(screen, (255, 255, 0), self.position, self.radius - 2)

    def update(self, dt):
        # Apply slight friction to slow down the orb
        self.velocity *= 0.98
        self.position += self.velocity * dt

    def is_collected_by(self, player):
        """Check if the orb is close enough to be collected by the player"""
        return self.position.distance_to(player.position) <= GOLD_ORB_COLLECTION_DISTANCE 