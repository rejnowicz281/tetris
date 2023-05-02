import random
import pygame

# Initialize pygame
pygame.init()

# Create screen
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title and Icon
pygame.display.set_caption("Tetris")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


class Block:
    def __init__(self):
        pass


class Game:
    def __init__(self):
        pass


# Game Loop
game = Game()
running = True
while running:
    # Ensure 60 FPS
    pygame.time.Clock().tick(60)

    # Background
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
