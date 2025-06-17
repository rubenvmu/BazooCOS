import pygame
from config import *
import time

class Shield:
    def __init__(self, player):
        self.player = player
        self.active = False
        self.activated_time = 0
        self.last_used = 0

    def activate(self):
        now = pygame.time.get_ticks()
        if not self.active and now - self.last_used > SHIELD_COOLDOWN:
            self.active = True
            self.activated_time = now
            self.last_used = now

    def update(self):
        if self.active:
            now = pygame.time.get_ticks()
            if now - self.activated_time > SHIELD_DURATION:
                self.active = False

    def draw(self, screen):
        if self.active:
            center = self.player.rect.center
            pygame.draw.circle(screen, CYAN, center, SHIELD_RADIUS, 3)

    def is_active(self):
        return self.active