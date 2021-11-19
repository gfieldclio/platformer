import pygame
import sys
from datetime import datetime
from pygame.locals import *
from constants import *
from sprites import Watson, watson


class GameOverScene():
    def __init__(self, displaysurface: pygame.Surface):
        self.displaysurface = displaysurface

    def setup(self):
        pygame.mixer.music.unload()
        pygame.mixer.music.load("assets/gameover.ogg")
        pygame.mixer.music.play()
        self.scene_start = datetime.now()
        self.initial_render = False
        self.watson = Watson()
        self.laugh = pygame.mixer.Sound("assets/laugh.mp3")
        self.laughed = False

    def render(self):
        duration = (datetime.now() - self.scene_start).total_seconds()
        if duration < 1:
            pass
        elif duration > 8:
            pygame.quit()
            sys.exit()
        elif duration > 4:
            if self.laughed == False:
                self.laugh.play()
                self.laughed = True
        else:
            if self.initial_render == False:
                color = pygame.Color(255, 0, 0, a=100)
                self.displaysurface.fill(color)
                font = pygame.font.SysFont("Verdana", FONT_SIZE * 3)
                text = font.render("Game Over", True, (0, 0, 0))
                text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/3))
                self.displaysurface.blit(text, text_rect)
                self.rendered_background = True

            self.displaysurface.blit(self.watson.surf, self.watson.rect)
            self.watson.move()

            pygame.display.update()
