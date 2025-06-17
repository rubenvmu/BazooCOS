import pygame
import random
from config import *
from objetos import crear_drop_random

class BossDron:
    boss_image = None
    laser_image = None

    @staticmethod
    def load_assets():
        if BossDron.boss_image is None:
            raw = pygame.image.load("sprites/bossdron.png").convert_alpha()
            BossDron.boss_image = pygame.transform.scale_by(raw, 0.2)
        if BossDron.laser_image is None:
            raw = pygame.image.load("sprites/ls.png").convert_alpha()
            BossDron.laser_image = pygame.transform.scale_by(raw, 0.06)

    def __init__(self):
        self.image = BossDron.boss_image.copy()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.health = 300  # 30 corazones (10 vida por corazón)
        self.opacity = 255
        self.dead = False
        self.last_teleport = pygame.time.get_ticks()
        self.last_shot = pygame.time.get_ticks()
        self.lasers = []
        self.teleport_cooldown = 10000  # 10 segundos
        self.shot_interval = 1500  # Dispara cada 1.5s
        self.invulnerable = False  # inmune a hackeo
        self.glow_surface = pygame.Surface((self.rect.width + 30, self.rect.height + 30), pygame.SRCALPHA)

    def update(self):
        now = pygame.time.get_ticks()

        # Teletransporte
        if now - self.last_teleport > self.teleport_cooldown:
            if self.rect.centerx < SCREEN_WIDTH // 2:
                self.rect.x = SCREEN_WIDTH - self.rect.width - 50
            else:
                self.rect.x = 50
            self.last_teleport = now

        # Disparar láser
        if now - self.last_shot > self.shot_interval:
            laser_rect = BossDron.laser_image.get_rect(midtop=self.rect.midbottom)
            self.lasers.append(laser_rect)
            self.last_shot = now

        # Mover láseres
        for laser in self.lasers:
            laser.y += 6

        self.lasers = [l for l in self.lasers if l.top < SCREEN_HEIGHT]

    def draw(self, screen):
        # Aura roja
        self.glow_surface.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.glow_surface, (255, 0, 0, 100), self.glow_surface.get_rect())
        screen.blit(self.glow_surface, (self.rect.x - 15, self.rect.y - 15))

        screen.blit(self.image, self.rect)

        for laser in self.lasers:
            screen.blit(BossDron.laser_image, laser)

    def hit(self):
        if not self.dead:
            self.health -= 10  # 10 de vida por disparo = 1 corazón
            if self.health <= 0:
                self.dead = True
                return True, []  # No dropea nada
        return False, []

    def collides_with(self, rect):
        return self.rect.colliderect(rect)

    def lasers_hit_player(self, player):
        for laser in self.lasers[:]:
            if laser.colliderect(player.rect):
                player.take_damage(10)
                self.lasers.remove(laser)

    def is_invulnerable_to_hack(self):
        return True