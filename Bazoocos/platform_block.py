import pygame
import random
import math
from config import *

def crop_to_visible_area(image):
    bounds = image.get_bounding_rect()
    if bounds.width == 0 or bounds.height == 0:
        return image
    return image.subsurface(bounds).copy()

class Platform:
    def __init__(self, x, y, scale=0.2):
        try:
            raw_img = pygame.image.load("sprites/antenaplataforma.png").convert_alpha()
            cropped = crop_to_visible_area(raw_img)

            if random.choice([True, False]):
                cropped = pygame.transform.flip(cropped, True, False)

            size = cropped.get_size()
            new_size = (int(size[0] * scale), int(size[1] * scale))
            self.image = pygame.transform.scale(cropped, new_size)
        except Exception as e:
            print("Error cargando plataforma:", e)
            self.image = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
            self.image.fill(GREEN)

        self.base_x = x
        self.base_y = y
        self.rect = self.image.get_rect(topleft=(x, y))

        # Máscara para detectar solo los píxeles visibles
        self.mask = pygame.mask.from_surface(self.image)

        # Movimiento flotante aleatorio
        self.float_amplitude = random.randint(3, 8)
        self.float_speed = random.uniform(0.8, 1.6)
        self.float_phase = random.uniform(0, math.pi * 2)

        self.lift_force = 0.6

    def update(self, dt):
        """Actualiza la posición con movimiento vertical aleatorio"""
        offset = math.sin(pygame.time.get_ticks() * 0.001 * self.float_speed + self.float_phase) * self.float_amplitude
        self.rect.y = self.base_y + int(offset)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def apply_levitation(self, player):
        """Levita al jugador si está tocando una parte opaca de la plataforma"""
        offset_x = player.rect.x - self.rect.x
        offset_y = player.rect.y - self.rect.y

        try:
            # Detectar colisión entre máscaras: solo si hay solapamiento de píxeles visibles
            if self.mask.overlap(pygame.mask.from_surface(player.get_current_sprite()), (offset_x, offset_y)):
                if abs(player.rect.bottom - self.rect.top) < 10:
                    player.rect.bottom = self.rect.top + int(player.rect.height * 0.33)
                    player.vel_y -= self.lift_force
                    if player.vel_y < -8:
                        player.vel_y = -8
        except:
            pass  # Si por alguna razón falla la detección, se ignora