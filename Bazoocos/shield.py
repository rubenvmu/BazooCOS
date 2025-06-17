import pygame

class Shield:
    def __init__(self, player):
        self.player = player
        self.active = False
        self.duration = 3000
        self.cooldown = 1000
        self.last_activated = -self.cooldown
        self.hold_start = 0

        try:
            full_image = pygame.image.load("sprites/shield.png").convert_alpha()
            self.image = pygame.transform.scale_by(full_image, 0.1)  # Escalado al 50%
        except:
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(self.image, (100, 100, 100, 150), (15, 15), 15)

    def update(self):
        mouse_buttons = pygame.mouse.get_pressed()
        now = pygame.time.get_ticks()

        if any(mouse_buttons):
            if not self.active and now - self.last_activated >= self.cooldown:
                self.active = True
                self.hold_start = now
                self.last_activated = now
                self.player.lanza.disabled = True
        else:
            if self.active:
                self.active = False
                self.player.lanza.disabled = False

        if self.active and now - self.hold_start > self.duration:
            self.active = False
            self.player.lanza.disabled = False

    def is_active(self):
        return self.active

    def draw(self, screen):
        if self.active:
            rect = self.image.get_rect(center=self.player.rect.center)
            screen.blit(self.image, rect)