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

        PT1 = Platform(
            WIDTH,
            FLOOR_HEIGHT,
            WIDTH/2,
            HEIGHT - (FLOOR_HEIGHT / 2)
        )
        PT1.moving = False
        PT1.surf.fill((255, 0, 0))
        state.highest_platform = HEIGHT - (FLOOR_HEIGHT / 2)

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
        font = pygame.font.SysFont("Verdana", FONT_SIZE)
        score = font.render(str(self.player.score), True, (123, 123, 255))
        score_rect = score.get_rect(center=(WIDTH/2, FONT_SIZE * 0.75))
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
            width = random.randrange(PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
            half_width = int(round(width / 2))
            x_pos = random.randrange(half_width, WIDTH - half_width)
            y_offset = random.randrange(PLATFORM_MIN_Y_GAP, PLATFORM_MAX_Y_GAP)
            y_pos = state.highest_platform - y_offset

            p = Platform(width, PLATFORM_HEIGHT, x_pos, y_pos)

            self.platforms.add(p)
            self.all_sprites.add(p)
            state.highest_platform = y_pos
