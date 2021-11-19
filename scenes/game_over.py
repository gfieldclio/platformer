import pygame
import sys
import time
from pygame.locals import *
from constants import *
from sprites import Player, Platform


class GameOverScene():
    def __init__(self, displaysurface):
        self.displaysurface = displaysurface

    def render(self):
        pygame.mixer.music.unload()
        pygame.mixer.music.load("assets/gameover.ogg")
        pygame.mixer.music.play()
        time.sleep(1)
        self.displaysurface.fill((255, 0, 0))
        font = pygame.font.SysFont("Verdana", FONT_SIZE * 3)
        text = font.render("Game Over", True, (0, 0, 0))
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        self.displaysurface.blit(text, text_rect)

        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        sys.exit()
