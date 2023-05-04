import random
import pygame

from pygame.math import Vector2

# Initialize pygame
pygame.init()

# Create screen
ROWS = 20
COLS = 10
CELL_SIZE = 35
SCREEN_MIDDLE = COLS / 2
SCREEN_WIDTH = COLS * CELL_SIZE
SCREEN_HEIGHT = ROWS * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title and Icon
pygame.display.set_caption("Tetris")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


class Block:
    def __init__(self, pos):
        self.previous_pos = None
        self.pos = pos

    def draw(self):
        x = self.pos.x * CELL_SIZE
        y = self.pos.y * CELL_SIZE
        rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0, 0, 255), rect)

    def move_down(self):
        self.pos.y += 1
        self.previous_pos = Vector2(self.pos.x, self.pos.y - 1)

    def move_left(self):
        self.pos.x -= 1
        self.previous_pos = Vector2(self.pos.x + 1, self.pos.y)

    def move_right(self):
        self.pos.x += 1
        self.previous_pos = Vector2(self.pos.x - 1, self.pos.y)


class Piece:
    BLOCK_COMBINATIONS = [
        # I
        [(SCREEN_MIDDLE, 0), (SCREEN_MIDDLE, 1),
         (SCREEN_MIDDLE, 2),
         (SCREEN_MIDDLE, 3)],

        # O
        [(SCREEN_MIDDLE, 0), (SCREEN_MIDDLE + 1, 0),
         (SCREEN_MIDDLE, 1),
         (SCREEN_MIDDLE + 1, 1)],

        # T
        [(SCREEN_MIDDLE - 1, 0), (SCREEN_MIDDLE, 0),
         (SCREEN_MIDDLE + 1, 0),
         (SCREEN_MIDDLE, 1)],

        # S
        [(SCREEN_MIDDLE, 0), (SCREEN_MIDDLE + 1, 0),
         (SCREEN_MIDDLE, 1),
         (SCREEN_MIDDLE - 1, 1)],

        # Z
        [(SCREEN_MIDDLE, 0), (SCREEN_MIDDLE + 1, 0),
         (SCREEN_MIDDLE, -1),
         (SCREEN_MIDDLE - 1, -1)],

        # J
        [(SCREEN_MIDDLE, 0), (SCREEN_MIDDLE, 1),
         (SCREEN_MIDDLE + 1, 1),
         (SCREEN_MIDDLE + 2, 1)],

        # L
        [(SCREEN_MIDDLE, 0), (SCREEN_MIDDLE, 1),
         (SCREEN_MIDDLE - 1, 1),
         (SCREEN_MIDDLE - 2, 1)]
    ]

    def __init__(self):
        self.blocks = []
        self.randomize_blocks()

    def randomize_blocks(self):
        positions = random.choice(self.BLOCK_COMBINATIONS)
        blocks = []
        [blocks.append(Block(Vector2(position))) for position in positions]
        self.blocks = blocks

    def draw(self):
        for block in self.blocks:
            block.draw()

    def move_left(self):
        for block in self.blocks:
            block.move_left()

    def move_right(self):
        for block in self.blocks:
            block.move_right()

    def move_down(self):
        for block in self.blocks:
            block.move_down()

    def set_previous_pos(self):
        for block in self.blocks:
            block.pos = block.previous_pos


class Game:
    def __init__(self):
        self.placed_blocks = []
        self.piece = Piece()

    def draw_placed_blocks(self):
        [block.draw() for block in self.placed_blocks]

    def new_piece(self):
        self.piece = Piece()

    def handle_horizontal_collision(self):
        placed_positions = [block.pos for block in self.placed_blocks]
        for piece_block in self.piece.blocks:
            if piece_block.pos.x < 0 or piece_block.pos.x > COLS - 1 or piece_block.pos in placed_positions:
                self.piece.set_previous_pos()

    def handle_vertical_collision(self):
        placed_positions = [block.pos for block in self.placed_blocks]
        for piece_block in self.piece.blocks:
            if piece_block.pos.y >= ROWS or piece_block.pos in placed_positions:
                self.piece.set_previous_pos()
                [self.placed_blocks.append(block) for block in self.piece.blocks]
                self.new_piece()

    def handle_clear(self):
        if self.placed_blocks:
            lowermost_row_blocks_count = 0
            for block in self.placed_blocks:
                if block.pos.y == ROWS - 1:
                    lowermost_row_blocks_count += 1  # If block is in the lowermost row, increment by 1
                if lowermost_row_blocks_count == COLS:  # If lowermost row is full
                    i = 0
                    while i in range(len(self.placed_blocks)):  # Delete all blocks from the lowermost row
                        if self.placed_blocks[i].pos.y == ROWS - 1:
                            del self.placed_blocks[i]
                        else:
                            i += 1

                    for block_b in self.placed_blocks:  # Move all blocks down
                        block_b.move_down()

                    return self.handle_clear()  # Function runs until lowermost row is not full


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
                game.piece.move_left()
                game.handle_horizontal_collision()
            elif event.key == pygame.K_RIGHT:
                game.piece.move_right()
                game.handle_horizontal_collision()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN]:
        game.piece.move_down()
        game.handle_vertical_collision()

    game.handle_clear()

    game.draw_placed_blocks()
    game.piece.draw()

    pygame.display.update()
