import pygame
from pygame.math import Vector2 as vec
from pygame.locals import *
from constants import *


class Watson(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.surf = pygame.image.load("assets/watson.png")
        self.surf = pygame.transform.scale(
            self.surf,
            (WATSON_WIDTH, WATSON_HEIGHT)
        )
        self.rect = self.surf.get_rect()
        self.rect.midbottom = vec(WIDTH / 2, HEIGHT + WATSON_HEIGHT)

    def move(self):
        if self.rect.bottom > HEIGHT:
            self.rect.bottom -= 4
