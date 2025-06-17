import pygame
from config import *

class MegaDrone:
    def __init__(self, x, y, level=1):
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ORANGE, (40, 40), 40)
        self.rect = self.image.get_rect(center=(x, y))

        self.health = 10 * level  # Aumenta según el nivel
        self.level = level
        self.speed = 1 + (0.3 * level)
        self.direction = 1

        self.damage = 1 * level

    def update(self):
        self.rect.x += self.direction * self.speed

        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # Dibujar barra de vida sobre el dron
        bar_width = self.rect.width
        bar_height = 6
        fill = int((self.health / (10 * self.level)) * bar_width)
        outline_rect = pygame.Rect(self.rect.left, self.rect.top - 10, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.left, self.rect.top - 10, fill, bar_height)

        pygame.draw.rect(screen, RED, fill_rect)
        pygame.draw.rect(screen, WHITE, outline_rect, 1)

    def hit(self, damage=1):
        self.health -= damage
        return self.health <= 0  # Devuelve True si muere