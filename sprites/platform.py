import pygame
import random
from constants import *


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(
            center=(
                x_pos,
                y_pos
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
