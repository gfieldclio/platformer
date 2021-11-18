import pygame
import random
from constants import *


class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((random.randint(50, 100), 12))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(0, WIDTH-10),
                random.randint(0, HEIGHT-30)
            )
        )
        self.score = True
        self.speed = random.randint(-1, 1)
        self.moving = random.choice([True, False])

    def move(self):
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.right > WIDTH or self.speed < 0 and self.rect.left < 0:
                self.speed *= -1
