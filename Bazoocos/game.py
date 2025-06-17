import pygame
from config import *
from player import Player

class Game:
    def __init__(self, screen):
        self.screen = screen

        try:
            self.bg = pygame.image.load("sprites/background.png").convert()
            self.bg = pygame.transform.scale(self.bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg.fill((20, 20, 40))

        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def handle_event(self, event):
        self.player.handle_event(event)

    def update(self, dt):
        self.player.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.player.draw(self.screen)