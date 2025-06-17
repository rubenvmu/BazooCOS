import pygame
import math
from config import *

class Projectile:
    def __init__(self, x, y, target_pos):
        self.x = x
        self.y = y

        dx = target_pos[0] - x
        dy = target_pos[1] - y
        angle = math.atan2(dy, dx)
        self.vel_x = math.cos(angle) * ROCKET_SPEED
        self.vel_y = math.sin(angle) * ROCKET_SPEED

        self.radius = PROJECTILE_RADIUS
        self.color = ORANGE
        self.rect = pygame.Rect(self.x, self.y, self.radius*2, self.radius*2)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.topleft = (int(self.x), int(self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_offscreen(self):
        return (self.x < 0 or self.x > SCREEN_WIDTH or
                self.y < 0 or self.y > SCREEN_HEIGHT)