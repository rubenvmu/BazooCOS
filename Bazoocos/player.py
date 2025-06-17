# player.py
import pygame
from config import *
from shield import Shield
from lanza import Lanza

class Player:
    def __init__(self, x, y):
        self.scale = 0.12
        self.sprite_idle = pygame.transform.scale_by(pygame.image.load("sprites/pj.png").convert_alpha(), self.scale)
        self.sprite_right = pygame.transform.scale_by(pygame.image.load("sprites/pj_lado.png").convert_alpha(), self.scale)
        self.sprite_left = pygame.transform.flip(self.sprite_right, True, False)
        self.sprite_jump = pygame.transform.scale_by(pygame.image.load("sprites/pj_jump.png").convert_alpha(), self.scale)
        self.rect = self.sprite_idle.get_rect(topleft=(x, y))
        self.heart_img = pygame.transform.scale(pygame.image.load("sprites/heart.png").convert_alpha(), (24, 24))

        self.vel = pygame.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        self.gravity = 0.3
        self.jet_power = -0.4
        self.max_fall_speed = 6
        self.max_rise_speed = -3

        self.facing_right = True
        self.health = 10
        self.max_health = 10
        self.shield = Shield(self)
        self.lanza = Lanza(self)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.shield.activate()

    def update(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        if keys[pygame.K_LEFT]:
            self.vel.x = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel.x = self.speed
            self.facing_right = True

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            self.vel.y += self.jet_power
            self.vel.y = max(self.vel.y, self.max_rise_speed)
        else:
            self.vel.y += self.gravity

        if self.vel.y > self.max_fall_speed:
            self.vel.y = self.max_fall_speed

        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel.y = 0

        self.shield.update()
        self.lanza.update()

    def draw(self, screen):
        keys = pygame.key.get_pressed()
        sprite = self.sprite_right if keys[pygame.K_RIGHT] else self.sprite_left if keys[pygame.K_LEFT] else self.sprite_idle
        screen.blit(sprite, self.rect)
        self.shield.draw(screen)
        self.draw_health(screen)
        self.lanza.draw(screen)

    def draw_health(self, screen):
        for i in range(self.health):
            screen.blit(self.heart_img, (SCREEN_WIDTH - (i + 1) * 28, 10))

    def take_damage(self, amount=1):
        if not self.shield.is_active():
            self.health = max(0, self.health - amount)

    def is_dead(self):
        return self.health <= 0
