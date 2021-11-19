import pygame
from pygame.math import Vector2 as vec
from pygame.locals import *
from constants import *


class Glider(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player

        self.surf = pygame.image.load("assets/glider.png")
        self.surf = pygame.transform.scale(self.surf, (60, 60))
        self.rect = self.surf.get_rect()
        self.facing = K_RIGHT

    def move(self):
        if self.facing != self.player.facing:
            self.facing = self.player.facing
            self.surf = pygame.transform.flip(
                self.surf, flip_x=True, flip_y=False)

        if self.player.is_gliding():
            self.rect.midbottom = self.player.pos - vec(0, 40)
        else:
            self.rect.midbottom = vec(-50, -50)
