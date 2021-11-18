import pygame
import random
import sys
import time
from pygame.locals import *
from constants import *
from sprites import Player, Platform

pygame.init()

FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

PT1 = Platform()
PT1.moving = False
PT1.surf = pygame.Surface((WIDTH, 20))
PT1.surf.fill((255, 0, 0))
PT1.rect = PT1.surf.get_rect(center=(WIDTH/2, HEIGHT - 10))

all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
platforms = pygame.sprite.Group()
platforms.add(PT1)
P1 = Player(platforms)
all_sprites.add(P1)

pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.play(loops=-1)


def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50, 100)
        half_width = int(round(width / 2))
        p = Platform()
        grouped = True
        while grouped:
            p.rect.center = (
                random.randrange(half_width, WIDTH - half_width),
                random.randrange(-150, -10)
            )
            grouped = check_grouped(p)
        platforms.add(p)
        all_sprites.add(p)


def check_grouped(platform):
    if pygame.sprite.spritecollideany(platform, platforms):
        return True
    else:
        platform_vertical_padding = 40
        for entity in platforms:
            if (abs(platform.rect.top - entity.rect.bottom) < platform_vertical_padding) or (abs(platform.rect.bottom - entity.rect.top) < platform_vertical_padding):
                return True
        return False


for x in range(random.randint(5, 6)):
    pl = Platform()
    grouped = True
    while grouped:
        pl.rect.center = (
            random.randint(0, WIDTH-10),
            random.randint(0, HEIGHT-30)
        )
        grouped = check_grouped(pl)
    platforms.add(pl)
    all_sprites.add(pl)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    displaysurface.fill((0, 0, 0))
    font = pygame.font.SysFont("Verdana", 20)
    score = font.render(str(P1.score), True, (123, 123, 255))
    score_rect = score.get_rect(center=(WIDTH/2, 15))
    displaysurface.blit(score, score_rect)

    P1.update()
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()
        plat_gen()

    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            pygame.mixer.music.unload()
            pygame.mixer.music.load("assets/gameover.ogg")
            pygame.mixer.music.play()
            time.sleep(1)
            displaysurface.fill((255, 0, 0))
            font = pygame.font.SysFont("Verdana", 50)
            text = font.render("Game Over", True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            displaysurface.blit(text, text_rect)

            pygame.display.update()
            time.sleep(3)
            pygame.quit()
            sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
