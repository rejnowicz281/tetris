import random
import pygame

from pygame.math import Vector2

# Initialize pygame
pygame.init()

# Create screen
ROWS = 20
COLS = 10
CELL_SIZE = 35
SCREEN_WIDTH = COLS * CELL_SIZE
SCREEN_HEIGHT = ROWS * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title and Icon
pygame.display.set_caption("Tetris")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


class Block:
    def __init__(self):
        self.previous_pivot = None
        self.pivot = Vector2(COLS / 2, 15)

    def draw(self):
        x = self.pivot.x * CELL_SIZE
        y = self.pivot.y * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0, 0, 255), rect)

    def move_down(self):
        self.pivot.y += 1
        self.previous_pivot = Vector2(self.pivot.x, self.pivot.y - 1)

    def move_left(self):
        self.pivot.x -= 1
        self.previous_pivot = Vector2(self.pivot.x + 1, self.pivot.y)

    def move_right(self):
        self.pivot.x += 1
        self.previous_pivot = Vector2(self.pivot.x - 1, self.pivot.y)


class Game:
    def __init__(self):
        self.placed_blocks = []
        self.block = Block()

    def draw_placed_blocks(self):
        for block in self.placed_blocks:
            block.draw()

    def new_block(self):
        self.block = Block()

    def handle_horizontal_collision(self):
        placed_pivots = [block.pivot for block in self.placed_blocks]
        if self.block.pivot.x < 0 or self.block.pivot.x > COLS - 1 or self.block.pivot in placed_pivots:
            self.block.pivot = self.block.previous_pivot

    def handle_vertical_collision(self):
        placed_pivots = [block.pivot for block in self.placed_blocks]
        if self.block.pivot.y >= ROWS or self.block.pivot in placed_pivots:
            self.block.pivot = self.block.previous_pivot
            self.placed_blocks.append(self.block)
            self.new_block()

    def handle_clear(self):
        if self.placed_blocks:
            current_row = ROWS - 1  # First, check the lowermost row
            while current_row >= 0:
                current_row_blocks = 0
                for block in self.placed_blocks:
                    if block.pivot.y == current_row:
                        current_row_blocks += 1  # If there is a block in the current row, increment by 1

                if current_row_blocks == COLS:  # If row is full
                    i = 0
                    while i in range(len(self.placed_blocks)):
                        if self.placed_blocks[i].pivot.y == current_row:
                            del self.placed_blocks[i]  # Delete all blocks from a row
                        else:
                            i += 1
                current_row -= 1


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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.block.move_left()
                game.handle_horizontal_collision()
            elif event.key == pygame.K_RIGHT:
                game.block.move_right()
                game.handle_horizontal_collision()
            elif event.key == pygame.K_DOWN:
                game.block.move_down()
                game.handle_vertical_collision()
            elif event.key == pygame.K_SPACE:
                for blokign in game.placed_blocks:
                    print(blokign.pivot.x, blokign.pivot.y)

    game.handle_clear()

    game.draw_placed_blocks()
    game.block.draw()

    pygame.display.update()
