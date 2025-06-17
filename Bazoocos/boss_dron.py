import pygame
import random
import math
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
        self.health = 50  # 5 corazones
        self.dead = False

        self.lasers = []
        self.last_shot = pygame.time.get_ticks()
        self.last_circle_shot = pygame.time.get_ticks()
        self.shot_interval = 1500
        self.circle_interval = 10000  # cada 10s

        self.speed = 2
        self.direction = random.choice([-1, 1])  # izquierda o derecha

        self.glow_surface = pygame.Surface((self.rect.width + 30, self.rect.height + 30), pygame.SRCALPHA)

    def update(self):
        now = pygame.time.get_ticks()

        # Movimiento lateral
        self.rect.x += self.speed * self.direction
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1

        # Disparo frontal normal
        if now - self.last_shot > self.shot_interval:
            laser_rect = BossDron.laser_image.get_rect(midtop=self.rect.midbottom)
            self.lasers.append({'rect': laser_rect, 'vx': 0, 'vy': 6})
            self.last_shot = now

        # Disparo circular
        if now - self.last_circle_shot > self.circle_interval:
            self.shoot_circle()
            self.last_circle_shot = now

        # Movimiento de proyectiles
        for laser in self.lasers:
            laser['rect'].x += laser['vx']
            laser['rect'].y += laser['vy']

        self.lasers = [l for l in self.lasers if l['rect'].bottom > 0 and l['rect'].top < SCREEN_HEIGHT and l['rect'].right > 0 and l['rect'].left < SCREEN_WIDTH]

    def shoot_circle(self):
        center_x = self.rect.centerx
        center_y = self.rect.bottom
        num_projectiles = 20
        angle_step = 2 * math.pi / num_projectiles
        speed = 4
        for i in range(num_projectiles):
            angle = i * angle_step
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            rect = BossDron.laser_image.get_rect(center=(center_x, center_y))
            self.lasers.append({'rect': rect, 'vx': vx, 'vy': vy})

    def draw(self, screen):
        # Aura roja
        self.glow_surface.fill((0, 0, 0, 0))
        pygame.draw.ellipse(self.glow_surface, (255, 0, 0, 100), self.glow_surface.get_rect())
        screen.blit(self.glow_surface, (self.rect.x - 15, self.rect.y - 15))

        screen.blit(self.image, self.rect)

        for laser in self.lasers:
            screen.blit(BossDron.laser_image, laser['rect'])

    def hit(self):
        if not self.dead:
            self.health -= 10  # 10 de vida por disparo = 1 corazón
            if self.health <= 0:
                self.dead = True
                return True, []
        return False, []

    def lasers_hit_player(self, player):
        for laser in self.lasers[:]:
            if laser['rect'].colliderect(player.rect):
                player.take_damage(10)
                self.lasers.remove(laser)

    def is_invulnerable_to_hack(self):
        return True