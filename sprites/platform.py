import pygame
import random
from constants import *
import state


class Platform(pygame.sprite.Sprite):
    def __init__(self, width, height, x_pos, y_pos):
        super().__init__()
        self.surf = pygame.Surface((width, height))
        self.rect = self.surf.get_rect(
            center=(
                x_pos,
                y_pos
            )
        )
        self.score = True
        self.speed = self._speed()
        self.moving = random.choice([True, False])
        self.disappearing = self._disappearing()
        self.exists = True

        if self.disappearing:
            self.surf.fill((255, 140, 0))
        else:
            self.surf.fill((0, 255, 0))

    def move(self):
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if self.speed > 0 and self.rect.right > WIDTH or self.speed < 0 and self.rect.left < 0:
                self.speed *= -1

    def fade(self):
        if self.disappearing:
            current_alpha = self.surf.get_alpha()
            if current_alpha == None:
                self.surf.set_alpha(255)
            elif current_alpha == 5:
                self.exists = False
            else:
                self.surf.set_alpha(current_alpha - 25)

    def _speed(self):
        speed = MOVING_PLATFORM_BASE_SPEED * state.score / 20
        speed = int(round(speed))
        speed = max(speed, 1)
        if random.choice([True, False]):
            speed *= -1

        return speed

    def _disappearing(self):
        if state.score > 100:
            return True

        chances = []
        for x in range(state.score):
            chances.append(True)
        for x in range(100 - state.score):
            chances.append(False)

        return random.choice(chances)
