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

        PT1 = Platform()
        PT1.moving = False
        PT1.surf = pygame.Surface((WIDTH, 20))
        PT1.surf.fill((255, 0, 0))
        PT1.rect = PT1.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))

        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(PT1)
        self.platforms = pygame.sprite.Group()
        self.platforms.add(PT1)

        self.player = Player(self.platforms)
        self.all_sprites.add(self.player)
        self.glider = Glider(self.player)
        self.all_sprites.add(self.glider)

        for x in range(6):
            pl = Platform()
            height = HEIGHT - ((x+1)*60) - random.randint(20, 40)
            pl.rect.center = (
                random.randint(0, WIDTH-10),
                height
            )
            self.platforms.add(pl)
            self.all_sprites.add(pl)

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
            self.player.pos.y += abs(self.player.vel.y)
            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
            self._generate_platforms()

        if self.player.rect.top > HEIGHT:
            for entity in self.all_sprites:
                entity.kill()
                state.scene = "game_over"

    def _generate_platforms(self):
        while len(self.platforms) < 7:
            width = random.randrange(50, 100)
            half_width = int(round(width / 2))
            p = Platform()
            grouped = True
            while grouped:
                p.rect.center = (
                    random.randrange(half_width, WIDTH - half_width),
                    random.randrange(-110, -10)
                )
                grouped = self._check_platform_grouping(p)
            self.platforms.add(p)
            self.all_sprites.add(p)

    def _check_platform_grouping(self, platform):
        if pygame.sprite.spritecollideany(platform, self.platforms):
            return True
        else:
            platform_vertical_padding = 30
            for entity in self.platforms:
                if (abs(platform.rect.top - entity.rect.bottom) < platform_vertical_padding) or (abs(platform.rect.bottom - entity.rect.top) < platform_vertical_padding):
                    return True
            return False
