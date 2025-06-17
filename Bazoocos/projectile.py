import pygame
import math
from config import *

class Projectile:
    def __init__(self, x, y, direction, size):
        self.base_pos = pygame.Vector2(x, y)
        self.direction = direction.normalize()
        self.perp = pygame.Vector2(-self.direction.y, self.direction.x)  # vector perpendicular
        self.speed = ROCKET_SPEED
        self.image = pygame.transform.scale(pygame.image.load("sprites/pr.png").convert_alpha(), size)
        self.rect = self.image.get_rect(center=self.base_pos)
        self.timer = 0
        self.alive = True
        self.amplitude = 8  # amplitud del zigzag
        self.frequency = 0.04  # frecuencia del zigzag

    def update(self):
        self.timer += 1
        self.base_pos += self.direction * self.speed
        offset = self.perp * math.sin(self.timer * self.frequency) * self.amplitude
        pos = self.base_pos + offset
        self.rect.center = (int(pos.x), int(pos.y))

        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.alive = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)