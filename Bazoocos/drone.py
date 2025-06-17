import pygame
import random
from config import *
from objetos import crear_drop_random

class Drone:
    drone_image = None

    @staticmethod
    def load_image():
        if Drone.drone_image is None:
            try:
                raw = pygame.image.load("sprites/dron.png").convert_alpha()
                Drone.drone_image = pygame.transform.scale_by(raw, 0.1)
            except Exception as e:
                print("[⚠] Error al cargar sprite de dron:", e)
                fallback = pygame.Surface((30, 30), pygame.SRCALPHA)
                pygame.draw.circle(fallback, RED, (15, 15), 15)
                Drone.drone_image = fallback

    def __init__(self, side):
        self.image = Drone.drone_image.copy()
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()

        if side == "left":
            self.rect.left = 0
            self.direction = 1
        else:
            self.rect.right = SCREEN_WIDTH
            self.direction = -1

        self.rect.y = random.randint(50, SCREEN_HEIGHT // 2)
        self.speed = random.uniform(1.0, 2.5)
        self.health = 1
        self.falling = False
        self.falling_dangerous = True
        self.opacity = 255
        self.fall_speed = 5
        self.fall_start_y = None
        self.dead = False

        # Cooldown de daño
        self.last_hit_time = 0  # en ms

    def update(self):
        if self.falling:
            if self.fall_start_y is None:
                self.fall_start_y = self.rect.y

            self.rect.y += self.fall_speed
            fall_distance = self.rect.y - self.fall_start_y
            fall_total = (SCREEN_HEIGHT - 50) - self.fall_start_y

            if fall_distance > fall_total / 3 and self.falling_dangerous:
                self.falling_dangerous = False
                self.opacity = 180
                self.image.set_alpha(self.opacity)

            if not self.falling_dangerous:
                self.opacity -= 8
                self.opacity = max(0, self.opacity)
                self.image.set_alpha(self.opacity)

            if self.rect.bottom >= SCREEN_HEIGHT - 50 or self.opacity <= 0:
                self.dead = True

        else:
            self.rect.x += self.direction * self.speed
            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.direction *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_drops(self, exclude_hackeo=False):
        return [crear_drop_random(self.rect.centerx, self.rect.bottom, exclude_hackeo)]

    def hit(self):
        self.health -= 1
        if self.health <= 0 and not self.falling:
            self.falling = True
            return True, self.get_drops(exclude_hackeo=False)
        return False, []

    def can_damage(self):
        """Retorna True si han pasado al menos 1 segundo desde el último daño."""
        return pygame.time.get_ticks() - self.last_hit_time >= 1000