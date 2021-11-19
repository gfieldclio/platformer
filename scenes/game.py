import pygame
import random
import sys
from pygame.locals import *
from constants import *
from sprites import Player, Platform, Glider
import state


class GameScene():
    def __init__(self, displaysurface):
        self.displaysurface = displaysurface

        PT1 = Platform(WIDTH, 20)
        PT1.moving = False
        PT1.surf.fill((255, 0, 0))
        PT1.rect = PT1.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))
        state.highest_platform = HEIGHT - 10

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(PT1)
        self.platforms = pygame.sprite.Group()
        self.platforms.add(PT1)

        self.player = Player(self.platforms)
        self.all_sprites.add(self.player)
        self.glider = Glider(self.player)
        self.all_sprites.add(self.glider)

        self._generate_platforms()

    def render(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.cancel_jump()

        self.displaysurface.fill((0, 0, 0))
        font = pygame.font.SysFont("Verdana", 20)
        score = font.render(str(self.player.score), True, (123, 123, 255))
        score_rect = score.get_rect(center=(WIDTH/2, 15))
        self.displaysurface.blit(score, score_rect)

        self.player.update()
        for entity in self.all_sprites:
            self.displaysurface.blit(entity.surf, entity.rect)
            entity.move()

        if self.player.rect.top <= HEIGHT / 3:
            y_screen_shift = abs(self.player.vel.y)
            self.player.pos.y += y_screen_shift
            for plat in self.platforms:
                plat.rect.y += y_screen_shift
                if plat.rect.top >= HEIGHT:
                    plat.kill()
            state.highest_platform += y_screen_shift
            self._generate_platforms()

        if self.player.rect.top > HEIGHT:
            for entity in self.all_sprites:
                entity.kill()
                state.scene = "game_over"

    def _generate_platforms(self):
        while state.highest_platform > 0:
            width = random.randrange(50, 100)
            half_width = int(round(width / 2))
            x_pos = random.randrange(half_width, WIDTH - half_width)
            y_pos = state.highest_platform - random.randrange(140, 160)
            p = Platform(width, 12)
            p.rect.center = (x_pos, y_pos)

            self.platforms.add(p)
            self.all_sprites.add(p)
            state.highest_platform = y_pos
