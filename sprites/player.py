import pygame
from pygame.math import Vector2 as vec
from pygame.locals import *
from constants import *


class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.platforms = platforms

        self.surf = pygame.image.load("assets/player.png")
        self.surf = pygame.transform.scale(self.surf, (40, 40))
        self.rect = self.surf.get_rect()

        self.pos = vec(10, 385)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0

    def move(self):
        self.acc = vec(0, 0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x += -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x += ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def update(self):
        platform = self._platform()
        if platform and self.vel.y > 0:
            self.jumping = False
            self.pos.y = platform.rect.top + 1
            self.vel.y = 0
            if platform.score:
                platform.score = False
                self.score += 1

    def jump(self):
        if self._platform():
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            self.jumping = False
            if self.vel.y < -3:
                self.vel.y = -3

    def _platform(self):
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in hits:
            if self.pos.y < platform.rect.bottom:
                return platform
