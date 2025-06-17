import pygame
from config import *
from shield import Shield
from lanza import Lanza

class Player:
    def __init__(self, x, y, game):
        self.game = game
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
        self.jet_power = -3
        self.max_fall_speed = 3
        self.max_rise_speed = -6
        self.facing_right = True

        self.health = 100
        self.max_health = 100
        self.health_regen_rate = 10 / (60 * 5)
        self.score = 0
        self.damage_timer = 0
        self.pending_drops = []

        self.speed_bonus = 1.0
        self.speed_timer = 0
        self.multi_shot = False
        self.multi_timer = 0
        self.magnet_active = False
        self.magnet_timer = 0

        self.shield = Shield(self)
        self.lanza = Lanza(self)

        self.stamina = 100
        self.max_stamina = 100
        self.stamina_regen_rate = 1.5
        self.stamina_per_shot = 2
        self.stamina_exhausted = False
        self.stamina_cooldown_timer = 0

        self.trail = []

    def handle_event(self, event):
        pass

    def update(self):
        keys = pygame.key.get_pressed()
        self.vel.x = 0

        if keys[pygame.K_LEFT]:
            self.vel.x = -self.speed * self.speed_bonus
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            self.vel.x = self.speed * self.speed_bonus
            self.facing_right = True
        if keys[pygame.K_UP]:
            self.vel.y += self.jet_power
            self.vel.y = max(self.vel.y, self.max_rise_speed)
        else:
            self.vel.y += self.gravity

        self.vel.y = min(self.vel.y, self.max_fall_speed)
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y

        # Añadir estela si hay boost
        if self.speed_bonus > 1.0:
            base_sprite = self.sprite_right if self.facing_right else self.sprite_left
            mask = pygame.mask.from_surface(base_sprite)
            trail_surf = pygame.Surface(base_sprite.get_size(), pygame.SRCALPHA)

            for x in range(base_sprite.get_width()):
                for y in range(base_sprite.get_height()):
                    if mask.get_at((x, y)):
                        trail_surf.set_at((x, y), (100, 200, 255, 80))  # azul brillante

            self.trail.append((trail_surf.copy(), self.rect.topleft, pygame.time.get_ticks()))
            if len(self.trail) > 8:
                self.trail.pop(0)

        # Limitar a pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.vel.y = 0

        now = pygame.time.get_ticks()
        if self.speed_bonus > 1.0 and now - self.speed_timer > 10000:
            self.speed_bonus = 1.0
        if self.multi_shot and now - self.multi_timer > 5000:
            self.multi_shot = False
        if self.magnet_active and now - self.magnet_timer > 5000:
            self.magnet_active = False

        if self.stamina_exhausted and now - self.stamina_cooldown_timer > 5000:
            self.stamina_exhausted = False
            self.stamina = self.max_stamina

        if not self.stamina_exhausted:
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen_rate * (1 / 60))

        if self.health < self.max_health:
            self.health += self.health_regen_rate
            self.health = min(self.health, self.max_health)

        self.shield.update()
        self.lanza.update()

    def draw(self, screen):
        now = pygame.time.get_ticks()

        # Dibujar estela eléctrica azul con transparencia
        for trail_surf, pos, t in self.trail:
            alpha = max(0, 120 - (now - t) // 8)
            if alpha > 0:
                temp = trail_surf.copy()
                temp.set_alpha(alpha)
                screen.blit(temp, pos)

        keys = pygame.key.get_pressed()
        sprite = self.sprite_right if keys[pygame.K_RIGHT] else self.sprite_left if keys[pygame.K_LEFT] else self.sprite_idle

        if now - self.damage_timer < 200:
            red_tint = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
            red_tint.fill((255, 0, 0, 120))
            temp = sprite.copy()
            temp.blit(red_tint, (0, 0))
            screen.blit(temp, self.rect)
        else:
            screen.blit(sprite, self.rect)

        self.shield.draw(screen)
        self.draw_health_bar(screen)
        self.draw_stamina_bar(screen)
        self.lanza.draw(screen)

    def draw_health_bar(self, screen):
        pygame.draw.rect(screen, (60, 60, 60), (10, 10, 100, 10))
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, 100 * self.health / self.max_health, 10))

    def draw_stamina_bar(self, screen):
        pygame.draw.rect(screen, (60, 60, 60), (10, 26, 100, 10))
        pygame.draw.rect(screen, (0, 200, 255), (10, 26, 100 * self.stamina / self.max_stamina, 10))

    def take_damage(self, amount=10):
        if not self.shield.is_active():
            self.health = max(0, self.health - amount)
            self.damage_timer = pygame.time.get_ticks()

    def is_dead(self):
        return self.health <= 0

    def is_shield_active(self):
        return self.shield.is_active()