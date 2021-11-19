import pygame
import sys
from datetime import datetime
from pygame.locals import *
from constants import *


class GameOverScene():
    def __init__(self, displaysurface):
        self.displaysurface = displaysurface

    def setup(self):
        pygame.mixer.music.unload()
        pygame.mixer.music.load("assets/gameover.ogg")
        pygame.mixer.music.play()
        self.scene_start = datetime.now()

    def render(self):
        duration = (datetime.now() - self.scene_start).total_seconds()
        if duration < 1:
            pass
        if duration > 4:
            pygame.quit()
            sys.exit()
        else:
            self.displaysurface.fill((255, 0, 0))
            font = pygame.font.SysFont("Verdana", FONT_SIZE * 3)
            text = font.render("Game Over", True, (0, 0, 0))
            text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
            self.displaysurface.blit(text, text_rect)

            pygame.display.update()
