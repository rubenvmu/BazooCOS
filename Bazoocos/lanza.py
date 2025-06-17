import pygame
from config import *
from projectile import Projectile

class Lanza:
    def __init__(self, player):
        self.player = player
        self.bazooka_img = pygame.transform.scale_by(
            pygame.image.load("sprites/lz.png").convert_alpha(), 0.135)

        self.projectiles = []
        self.base_shoot_delay = 500  # milisegundos base
        self.last_shot = 0

    def update(self):
        now = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if self.player.is_shield_active():
            return  # No disparar con escudo

        # Aumento de cadencia: 3% menos delay por microchip
        chip_factor = 0.03 * getattr(self.player, "microchips", 0)
        adjusted_delay = max(150, self.base_shoot_delay * (1 - chip_factor))  # mínimo 150ms

        if keys[pygame.K_SPACE] and now - self.last_shot > adjusted_delay:
            if self.player.stamina < self.player.stamina_per_shot:
                self.player.stamina_exhausted = True
                self.player.stamina_cooldown_timer = now
                return

            self.player.stamina -= self.player.stamina_per_shot
            self.last_shot = now

            mouse = pygame.mouse.get_pos()
            direction = pygame.Vector2(mouse) - self.player.rect.center
            offset = pygame.Vector2(25, self.player.rect.height * 0.07)
            if not self.player.facing_right:
                offset.x *= -1
            fire_pos = self.player.rect.center + offset
            size = self.bazooka_img.get_size()

            if self.player.multi_shot:
                angles = [
                    direction,
                    pygame.Vector2(0, -1),
                    pygame.Vector2(0, 1),
                    pygame.Vector2(1, 1),
                    pygame.Vector2(-1, 1)
                ]
                for dir in angles:
                    self.projectiles.append(Projectile(fire_pos.x, fire_pos.y, dir, size))
            else:
                self.projectiles.append(Projectile(fire_pos.x, fire_pos.y, direction, size))

        for p in self.projectiles:
            p.update()

        self.projectiles = [p for p in self.projectiles if p.alive]

    def draw(self, screen):
        if not self.player.is_shield_active():
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