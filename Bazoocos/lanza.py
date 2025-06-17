import pygame
from config import *

class Projectile:
    def __init__(self, x, y, direction, size):
        self.image = pygame.image.load("sprites/pr.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction.normalize()
        self.speed = 10
        self.damage = 1
        self.alive = True

    def update(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        if (self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or
            self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT):
            self.alive = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Lanza:
    def __init__(self, player):
        self.player = player
        self.bazooka_img = pygame.transform.scale_by(
            pygame.image.load("sprites/lz.png").convert_alpha(), 0.135)

        self.projectiles = []
        self.shoot_delay = 500  # milisegundos
        self.last_shot = 0

    def update(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and now - self.last_shot > self.shoot_delay:
            mouse = pygame.mouse.get_pos()
            direction = pygame.Vector2(mouse) - self.player.rect.center
            offset = pygame.Vector2(25, self.player.rect.height * 0.07)
            if not self.player.facing_right:
                offset.x *= -1
            fire_pos = self.player.rect.center + offset
            size = self.bazooka_img.get_size()
            self.projectiles.append(Projectile(fire_pos.x, fire_pos.y, direction, size))
            self.last_shot = now

        for p in self.projectiles:
            p.update()
        self.projectiles = [p for p in self.projectiles if p.alive]

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        direction = pygame.Vector2(mouse) - self.player.rect.center
        angle = direction.angle_to((1, 0))

        rotated = pygame.transform.rotate(self.bazooka_img, -angle)
        offset = pygame.Vector2(25, self.player.rect.height * 0.07)
        if not self.player.facing_right:
            offset.x *= -1
        pos = self.player.rect.center + offset
        rect = rotated.get_rect(center=pos)
        screen.blit(rotated, rect)

        for p in self.projectiles:
            p.draw(screen)