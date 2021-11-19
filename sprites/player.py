import pygame
from pygame.math import Vector2 as vec
from pygame.locals import *
from constants import *
import state


class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.platforms = platforms

        self.surf = pygame.image.load("assets/player.png")
        self.surf = pygame.transform.scale(
            self.surf, (PLAYER_SIZE, PLAYER_SIZE))
        self.rect = self.surf.get_rect()

        self.pos = vec(PLAYER_SIZE/2, HEIGHT - FLOOR_HEIGHT)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.gliding = False
        self.facing = K_RIGHT
        self.score = 0

    def move(self):
        self.acc = vec(0, GRAVITY)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x += -ACCELERATION
            if self.facing == K_RIGHT:
                self.surf = pygame.transform.flip(
                    self.surf, flip_x=True, flip_y=False)
                self.facing = K_LEFT
        if pressed_keys[K_RIGHT]:
            self.acc.x += ACCELERATION
            if self.facing == K_LEFT:
                self.surf = pygame.transform.flip(
                    self.surf, flip_x=True, flip_y=False)
                self.facing = K_RIGHT

        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc
        if self.is_gliding():
            self.vel.y = min(self.acc.y, GLIDER_VELOCITY)

        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

    def update(self):
        platform = self._platform()
        if platform and self.vel.y > 0:
            self.gliding = False
            self.pos.y = platform.rect.top + 1
            self.vel.y = 0
            if platform.score:
                platform.score = False
                state.score += 1

    def jump(self):
        self.gliding = True
        if self._platform():
            self.vel.y = JUMP_VELOCITY

    def cancel_jump(self):
        self.gliding = False
        if self.vel.y < JUMP_CANCEL_VELOCITY:
            self.vel.y = JUMP_CANCEL_VELOCITY

    def is_gliding(self):
        return self.gliding and self.vel.y > 0

    def _platform(self):
        hits = pygame.sprite.spritecollide(self, self.platforms, False)
        for platform in hits:
            if self.pos.y < platform.rect.bottom:
                return platform
