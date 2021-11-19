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


def get_game_scene():
    if state.scene == "game":
        return game_scene
    elif state.scene == "game_over":
        return game_over_scene


while True:
    scene = get_game_scene()

    if state.previous_scene != state.scene:
        scene.setup()
        state.previous_scene = state.scene

    scene.render()

    pygame.display.update()
    FramePerSec.tick(FPS)
