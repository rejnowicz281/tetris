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


def draw_text(x, y, text, font=pygame.font.Font('freesansbold.ttf', 32), color=(255, 255, 255)):
    content = font.render(text, True, color)
    screen.blit(content, (x, y))


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
        rect = pygame.Rect(x, y, CELL_SIZE - 1, CELL_SIZE - 1)
        pygame.draw.rect(screen, (0, 0, 255), rect)

    def move_down(self):
        self.move(0, 1)

    def move_left(self):
        self.move(-1, 0)

    def move_right(self):
        self.move(1, 0)

    def move(self, x, y):
        self.update_previous_pos()
        self.pos.x += x
        self.pos.y += y

    def move_to(self, x, y):
        self.update_previous_pos()
        self.pos.x = x
        self.pos.y = y

    def update_previous_pos(self):
        self.previous_pos = Vector2(self.pos.x, self.pos.y)


class Piece:
    BLOCK_COMBINATIONS = {
        "I": [(SCREEN_MIDDLE - 2, 0), (SCREEN_MIDDLE - 1, 0),
              (SCREEN_MIDDLE, 0),
              (SCREEN_MIDDLE + 1, 0)],

        "O": [(SCREEN_MIDDLE - 1, 0), (SCREEN_MIDDLE, 0),
              (SCREEN_MIDDLE - 1, 1),
              (SCREEN_MIDDLE, 1)],

        "T": [(SCREEN_MIDDLE - 1, 0), (SCREEN_MIDDLE, 0),
              (SCREEN_MIDDLE + 1, 0),
              (SCREEN_MIDDLE, 1)],

        "S": [(SCREEN_MIDDLE - 1, 0), (SCREEN_MIDDLE, 0),
              (SCREEN_MIDDLE - 1, 1),
              (SCREEN_MIDDLE - 2, 1)],

        "Z": [(SCREEN_MIDDLE - 1, 0), (SCREEN_MIDDLE, 0),
              (SCREEN_MIDDLE, 1),
              (SCREEN_MIDDLE + 1, 1)],

        "J": [(SCREEN_MIDDLE - 1, 0), (SCREEN_MIDDLE - 1, 1),
              (SCREEN_MIDDLE, 1),
              (SCREEN_MIDDLE + 1, 1)],

        "L": [(SCREEN_MIDDLE, 0), (SCREEN_MIDDLE, 1),
              (SCREEN_MIDDLE - 1, 1),
              (SCREEN_MIDDLE - 2, 1)]
    }

    def __init__(self):
        self.shape = None
        self.blocks = []
        self.initialize_blocks()

    def initialize_blocks(self):
        random_shape = random.choice(list(self.BLOCK_COMBINATIONS.keys()))
        combination = self.BLOCK_COMBINATIONS[random_shape]
        blocks = [(Block(Vector2(position))) for position in combination]
        self.blocks = blocks
        self.shape = random_shape

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

    def rotate(self):
        if self.shape != "O":
            pivot = self.blocks[1].pos
            for block in self.blocks:
                translate = block.pos - pivot
                rotated = translate.rotate(90) + pivot
                block.move_to(rotated.x, rotated.y)


class Game:
    def __init__(self):
        self.placed_blocks = []
        self.pieces_counter = {
            "I": 0,
            "O": 0,
            "T": 0,
            "S": 0,
            "Z": 0,
            "J": 0,
            "L": 0
        }
        self.bag = []
        self.refill_bag()
        self.queue = []
        self.refill_queue()
        self.state = "running"

    def current_piece(self):
        return self.queue[0]

    def pieces_preview(self):
        return self.queue[1:]

    def refill_bag(self):
        if not len(self.bag):
            while len(self.bag) < len(Piece.BLOCK_COMBINATIONS):
                random_piece = Piece()
                current_shapes = [piece.shape for piece in self.bag]
                if random_piece.shape not in current_shapes:
                    self.bag.append(random_piece)

    def refill_queue(self):
        while len(self.queue) < 4:
            self.queue.append(self.bag[0])
            del self.bag[0]

    def draw_placed_blocks(self):
        [block.draw() for block in self.placed_blocks]

    def game_over_check(self):
        placed_positions = [block.pos for block in self.placed_blocks]
        for piece_block in self.current_piece().blocks:
            if piece_block.pos in placed_positions and piece_block.previous_pos is None:
                self.state = "game_over"
                break

    def handle_horizontal_collision(self):
        placed_positions = [block.pos for block in self.placed_blocks]
        for piece_block in self.current_piece().blocks:
            if piece_block.pos.x < 0 or piece_block.pos.x > COLS - 1 or piece_block.pos in placed_positions:
                self.current_piece().set_previous_pos()
                break

    def handle_vertical_collision(self):
        placed_positions = [block.pos for block in self.placed_blocks]
        for piece_block in self.current_piece().blocks:
            if piece_block.pos.y >= ROWS or piece_block.pos in placed_positions:
                self.current_piece().set_previous_pos()
                [self.placed_blocks.append(block) for block in self.current_piece().blocks]
                self.handle_clear()
                self.pieces_counter[self.current_piece().shape] += 1
                del self.queue[0]
                self.refill_bag()
                self.refill_queue()
                self.game_over_check()
                break

    def handle_rotation_collision(self):
        placed_positions = [block.pos for block in self.placed_blocks]
        for piece_block in self.current_piece().blocks:
            if piece_block.pos.x < 0 or piece_block.pos.x > COLS - 1 or piece_block.pos.y >= ROWS or piece_block.pos in placed_positions:
                self.current_piece().set_previous_pos()
                break

    def handle_clear(self, current_row=ROWS - 1):
        if self.placed_blocks and current_row >= 0:
            current_row_blocks_count = 0
            for block in self.placed_blocks:
                if block.pos.y == current_row:
                    current_row_blocks_count += 1  # If block is in the current row, increment by 1

                if current_row_blocks_count == COLS:  # If current row is full
                    i = 0
                    while i in range(len(self.placed_blocks)):  # Delete all blocks from the current row
                        if self.placed_blocks[i].pos.y == current_row:
                            del self.placed_blocks[i]
                        else:
                            i += 1

                    for block_b in self.placed_blocks:  # Move all blocks above the current row down
                        if block_b.pos.y < current_row:
                            block_b.move_down()

                    return self.handle_clear()  # Function runs until current row is not full

            if current_row_blocks_count != COLS:  # If current row isn't full, check the next one
                return self.handle_clear(current_row - 1)


# Game Loop
last_update_time = pygame.time.get_ticks()
game = Game()
running = True
while running:
    fall_speed = 800
    # Ensure 60 FPS
    pygame.time.Clock().tick(60)

    # Background
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and game.state == "running":
            if event.key == pygame.K_LEFT:
                game.current_piece().move_left()
                game.handle_horizontal_collision()
            elif event.key == pygame.K_RIGHT:
                game.current_piece().move_right()
                game.handle_horizontal_collision()
            elif event.key == pygame.K_UP:
                game.current_piece().rotate()
                game.handle_rotation_collision()
    keys = pygame.key.get_pressed()

    if keys[pygame.K_DOWN]:
        fall_speed = 50

    game.current_piece().draw()
    game.draw_placed_blocks()

    current_time = pygame.time.get_ticks()
    elapsed_time = current_time - last_update_time

    if game.state == "running":
        if elapsed_time >= fall_speed:
            game.current_piece().move_down()
            game.handle_vertical_collision()
            last_update_time = current_time
    else:
        draw_text(10, 10, "GAME OVER")

    pygame.display.update()
