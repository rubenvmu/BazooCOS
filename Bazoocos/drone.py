import pygame
import random
from config import *

class Drone:
    def __init__(self, x, y):
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (20, 20), 20)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = random.choice([-1, 1])
        self.speed = random.uniform(1.0, 2.5)
        self.health = 1

    def update(self):
        self.rect.x += self.direction * self.speed

        # Rebote horizontal
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def hit(self):
        self.health -= 1
        return self.health <= 0  # Devuelve True si muere