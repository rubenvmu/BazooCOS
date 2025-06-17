import pygame
import random
from config import *
from player import Player
from drone import Drone
from boss_dron import BossDron

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("consolas", 24, bold=True)

        try:
            self.bg = pygame.transform.scale(
                pygame.image.load("sprites/background.png").convert(),
                (SCREEN_WIDTH, SCREEN_HEIGHT)
            )
        except:
            self.bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg.fill((20, 20, 40))

        self.microchip_icon = pygame.transform.scale(
            pygame.image.load("sprites/microchip.png").convert_alpha(), (28, 28))

        self.hackeo_flash_img = pygame.transform.scale(
            pygame.image.load("sprites/hackeo.png").convert_alpha(),
            (SCREEN_WIDTH, SCREEN_HEIGHT)
        )
        self.hackeo_flash_alpha = 0
        self.hackeo_flash_timer = 0

        Drone.load_image()
        BossDron.load_assets()
        self.reset_game()

    def reset_game(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, self)
        self.drones = []
        self.drops = []
        self.boss = None
        self.spawn_timer = 0
        self.spawn_interval = 2000
        self.death_time = None

    def spawn_drone(self):
        self.drones.append(Drone(random.choice(["left", "right"])))

    def maybe_spawn_boss(self):
        if self.player.score >= 250 and self.player.score % 250 == 0 and self.boss is None:
            self.boss = BossDron()

    def handle_event(self, event):
        self.player.handle_event(event)

    def update(self, dt):
        if self.player.is_dead():
            if self.death_time is None:
                self.death_time = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.death_time > 2000:
                self.reset_game()
            return

        self.player.update()
        self.spawn_timer += dt
        self.maybe_spawn_boss()

        if self.spawn_timer >= self.spawn_interval:
            self.spawn_drone()
            self.spawn_timer = 0

        if self.player.score > 0 and self.player.score % 10 == 0:
            self.spawn_interval = max(500, self.spawn_interval - 50)

        for drone in self.drones:
            drone.update()
            if drone.falling_dangerous and drone.rect.colliderect(self.player.rect):
                if drone.can_damage():
                    self.player.take_damage(10)
                    drone.last_hit_time = pygame.time.get_ticks()

        self.drones = [d for d in self.drones if not d.dead]

        new_projectiles = []
        for p in self.player.lanza.projectiles:
            hit = False
            for drone in self.drones[:]:
                if drone.rect.colliderect(p.rect):
                    muerto, dropeos = drone.hit()
                    if muerto:
                        self.drops.extend(dropeos)
                        self.player.score += 1
                    hit = True
                    break

            if self.boss and p.rect.colliderect(self.boss.rect):
                if not self.boss.is_invulnerable_to_hack():
                    self.boss.health -= 1
                else:
                    self.boss.hit()
                hit = True

            if not hit:
                new_projectiles.append(p)
        self.player.lanza.projectiles = [p for p in new_projectiles if p.alive]

        for drop in self.drops:
            drop.update(self.player)
            if drop.rect.colliderect(self.player.rect):
                drop.apply(self.player, self.drones)
                drop.active = False

        self.drops = [d for d in self.drops if d.active]

        if self.player.pending_drops:
            self.drops.extend(self.player.pending_drops)
            self.player.pending_drops = []

        if self.hackeo_flash_alpha > 0:
            elapsed = pygame.time.get_ticks() - self.hackeo_flash_timer
            self.hackeo_flash_alpha = max(0, 255 - int((elapsed / 3000) * 255))

        if self.boss:
            self.boss.update()
            self.boss.lasers_hit_player(self.player)
            if self.boss.rect.colliderect(self.player.rect):
                self.player.take_damage(20)
            if self.boss.dead:
                self.boss = None
                self.player.score += 10

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.player.draw(self.screen)

        for drone in self.drones:
            drone.draw(self.screen)

        if self.boss:
            self.boss.draw(self.screen)
            # Dibujar barra de vida del boss
            health_bar_width = SCREEN_WIDTH - 100
            health_ratio = self.boss.health / 300
            pygame.draw.rect(self.screen, (100, 0, 0), (50, 30, health_bar_width, 20))
            pygame.draw.rect(self.screen, (255, 0, 0), (50, 30, int(health_bar_width * health_ratio), 20))
            self.screen.blit(self.font.render("Boss Dron", True, (255, 255, 255)), (50, 5))

        for drop in self.drops:
            drop.draw(self.screen)

        self.screen.blit(self.microchip_icon, (10, 10))
        self.screen.blit(self.font.render(f"x {self.player.score}", True, (255, 255, 255)), (46, 12))

        if self.hackeo_flash_alpha > 0:
            overlay = self.hackeo_flash_img.copy()
            overlay.set_alpha(self.hackeo_flash_alpha)
            self.screen.blit(overlay, (0, 0))

        if self.player.is_dead():
            death_text = self.font.render("GAME OVER - Reiniciando...", True, (255, 100, 100))
            self.screen.blit(death_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 20))