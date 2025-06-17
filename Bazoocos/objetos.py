import pygame
import random
from config import *

class Loot:
    def __init__(self, x, y, image_path, effect_name):
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, 0.06)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = 2
        self.effect_name = effect_name
        self.active = True

    def update(self, player):
        self.rect.y += self.vel_y
        if player.magnet_active:
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            dist = max(1, (dx**2 + dy**2)**0.5)
            self.rect.x += int(dx / dist * 3)
            self.rect.y += int(dy / dist * 3)
        if self.rect.top > SCREEN_HEIGHT:
            self.active = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def apply(self, player, drones): 
        pass


class LootHackeo(Loot):
    def __init__(self, x, y):
        super().__init__(x, y, "sprites/loot_hackeo.png", "hackeo")

    def apply(self, player, drones):
        from objetos import Microchip
        nuevos_drops = []
        for d in drones:
            if not d.falling:
                d.health = 0
                d.falling = True
                d.direction *= -1
                d.speed *= 2
                nuevos_drops.append(Microchip(d.rect.centerx, d.rect.bottom))
        player.score += len(nuevos_drops)
        player.pending_drops.extend(nuevos_drops)

        # Efecto visual de hackeo
        game = player.game
        game.hackeo_flash_alpha = 255
        game.hackeo_flash_timer = pygame.time.get_ticks()


class LootVelocidad(Loot):
    def __init__(self, x, y):
        super().__init__(x, y, "sprites/loot_velocidad.png", "velocidad")

    def apply(self, player, drones):
        player.speed_bonus = 3.0
        player.speed_timer = pygame.time.get_ticks()


class LootMultiproyectil(Loot):
    def __init__(self, x, y):
        super().__init__(x, y, "sprites/loot_multi.png", "multiproyectil")

    def apply(self, player, drones):
        player.multi_shot = True
        player.multi_timer = pygame.time.get_ticks()


class LootMagnetismo(Loot):
    def __init__(self, x, y):
        super().__init__(x, y, "sprites/loot_magnet.png", "magnetismo")

    def apply(self, player, drones):
        player.magnet_active = True
        player.magnet_timer = pygame.time.get_ticks()


class Microchip(Loot):
    def __init__(self, x, y):
        super().__init__(x, y, "sprites/microchip.png", "microchip")

    def apply(self, player, drones):
        player.score += 1


def crear_drop_random(x, y, exclude_hackeo=False):
    prob = random.randint(1, 100)
    if prob <= 5 and not exclude_hackeo:
        return LootHackeo(x, y)
    elif prob <= 15:
        return LootMultiproyectil(x, y)
    elif prob <= 20:
        return LootVelocidad(x, y)
    elif prob <= 25:
        return LootMagnetismo(x, y)
    else:
        return Microchip(x, y)