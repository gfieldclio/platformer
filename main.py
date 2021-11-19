import pygame
from pygame.locals import *
from constants import *
from scenes import GameScene, GameOverScene
import state

pygame.init()

FramePerSec = pygame.time.Clock()

pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.play(loops=-1)

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

game_over_scene = GameOverScene(displaysurface)
game_scene = GameScene(displaysurface)

while True:
    if state.scene == "game":
        game_scene.render()
    elif state.scene == "game_over":
        game_over_scene.render()

    pygame.display.update()
    FramePerSec.tick(FPS)
