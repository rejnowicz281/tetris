import random
import pygame

from pygame.math import Vector2

# Initialize pygame
pygame.init()

# Global Screen Variables
CELL_SIZE = 35

GAME_ROWS = 20
GAME_COLS = 10
GAME_WIDTH = GAME_COLS * CELL_SIZE
GAME_HEIGHT = GAME_ROWS * CELL_SIZE

SCREEN_WIDTH = GAME_WIDTH * 2.5
SCREEN_HEIGHT = GAME_HEIGHT * 1.1
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))


def draw_text(x, y, text, surface=screen, font=pygame.font.Font('freesansbold.ttf', 32), color=(255, 255, 255)):
    content = font.render(text, True, color)
    surface.blit(content, (x, y))


def draw_game_window():
    game_rect = game_surface.get_rect()
    pygame.draw.rect(game_surface, (0, 150, 0), (game_rect.x, game_rect.y, game_rect.width, game_rect.height), 1)
    screen.blit(game_surface, ((SCREEN_WIDTH - GAME_WIDTH) / 2, (SCREEN_HEIGHT - GAME_HEIGHT) / 2))

    game_surface.fill((10, 10, 10))


# Title and Icon
pygame.display.set_caption("Tetris")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)


class Block:
    def __init__(self, pos, color):
        self.previous_pos = None
        self.pos = pos
        self.color = color

    def draw(self, surface=game_surface, offset_x=0, offset_y=0):
        x = self.pos.x * CELL_SIZE + offset_x
        y = self.pos.y * CELL_SIZE + offset_y
        rect = pygame.Rect(x, y, CELL_SIZE - 2, CELL_SIZE - 2)
        pygame.draw.rect(surface, self.color, rect)

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
        "I": {
            "position": [(- 2, 0), (- 1, 0),
                         (0, 0),
                         (+ 1, 0)],
            "color": (255, 0, 0)
        },
        "O": {
            "position": [(- 1, 0), (0, 0),
                         (- 1, 1),
                         (0, 1)],
            "color": (0, 255, 0)
        },
        "T": {
            "position": [(- 1, 0), (0, 0),
                         (+ 1, 0),
                         (0, 1)],
            "color": (0, 0, 255)
        },
        "S": {
            "position": [(- 1, 0), (0, 0),
                         (- 1, 1),
                         (- 2, 1)],
            "color": (255, 255, 0)
        },
        "Z": {
            "position": [(- 1, 0), (0, 0),
                         (0, 1),
                         (+ 1, 1)],
            "color": (255, 255, 255)
        },
        "J": {
            "position": [(- 1, 0), (- 1, 1),
                         (0, 1),
                         (+ 1, 1)],
            "color": (106, 90, 205)
        },
        "L": {
            "position": [(0, 0), (0, 1),
                         (- 1, 1),
                         (- 2, 1)],
            "color": (0, 250, 154)
        }
    }

    def __init__(self, shape=None):
        self.shape = shape
        self.blocks = []
        self.initialize_blocks()

    def initialize_blocks(self):
        if self.shape is None:
            self.shape = random.choice(list(self.BLOCK_COMBINATIONS.keys()))

        combination = self.BLOCK_COMBINATIONS[self.shape]
        color = combination["color"]
        blocks = [(Block(Vector2(position[0] + GAME_COLS / 2, position[1]), color)) for position in
                  combination["position"]]
        self.blocks = blocks

    def draw(self, surface=game_surface, offset_x=0, offset_y=0):
        for block in self.blocks:
            block.draw(surface, offset_x, offset_y)

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
        self.score = 0
        self.high_score = 0
        self.load_high_score()
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

    def load_high_score(self):
        try:
            with open("high_score.txt", "r") as high_score_file:
                self.high_score = int(high_score_file.read())
        except FileNotFoundError:
            self.high_score = 0

    def save_high_score(self):
        with open("high_score.txt", "w") as high_score_file:
            high_score_file.write(str(self.high_score))

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
            if piece_block.pos.x < 0 or piece_block.pos.x > GAME_COLS - 1 or piece_block.pos in placed_positions:
                self.current_piece().set_previous_pos()
                break

    def handle_vertical_collision(self):
        placed_positions = [block.pos for block in self.placed_blocks]
        for piece_block in self.current_piece().blocks:
            if piece_block.pos.y >= GAME_ROWS or piece_block.pos in placed_positions:
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
            if piece_block.pos.x < 0 or piece_block.pos.x > GAME_COLS - 1 or piece_block.pos.y >= GAME_ROWS or piece_block.pos in placed_positions:
                self.current_piece().set_previous_pos()
                break

    def handle_clear(self, lines=0, current_row=GAME_ROWS - 1):
        if self.placed_blocks and current_row >= 0:
            current_row_blocks_count = 0
            for block in self.placed_blocks:
                if block.pos.y == current_row:
                    current_row_blocks_count += 1  # If block is in the current row, increment by 1

                if current_row_blocks_count == GAME_COLS:  # If current row is full
                    i = 0
                    while i in range(len(self.placed_blocks)):  # Delete all blocks from the current row
                        if self.placed_blocks[i].pos.y == current_row:
                            del self.placed_blocks[i]
                        else:
                            i += 1

                    for block_b in self.placed_blocks:  # Move all blocks above the current row down
                        if block_b.pos.y < current_row:
                            block_b.move_down()

                    return self.handle_clear(lines + 1)  # Function runs until current row is not full

            if current_row_blocks_count != GAME_COLS:  # If current row isn't full, check the next one
                if lines == 1:
                    self.score += 40
                elif lines == 2:
                    self.score += 100
                elif lines == 3:
                    self.score += 300
                elif lines == 4:
                    self.score += 1000
                return self.handle_clear(0, current_row - 1)

    def draw_pieces_preview(self):
        draw_text(650, 300, "Next Pieces")
        for index, piece in enumerate(self.pieces_preview()):
            piece.draw(screen, 570, (150 * (index + 1))+200)

    def draw_pieces_counter(self):
        draw_text(10, 30, "Pieces Counter")
        for index, piece in enumerate(self.pieces_counter):
            Piece(piece).draw(screen, -80, 90 * (index + 1))
            draw_text(180, 90 * (index + 1), str(self.pieces_counter[piece]))

    def draw_score(self):
        draw_text(650, 40, "Score")
        draw_text(650, 80, str(self.score))

    def draw_high_score(self):
        draw_text(650, 130, "High Score")
        draw_text(650, 180, str(self.high_score))

    def increase_score(self, amount):
        self.score += amount
        if self.score > self.high_score:
            self.high_score = self.score


# Game Loop
last_update_time = pygame.time.get_ticks()
game = Game()
running = True
while running:
    fall_speed = 800
    # Ensure 60 FPS
    pygame.time.Clock().tick(60)

    # Screen
    screen.fill((0, 0, 0))

    draw_game_window()
    game.draw_pieces_preview()
    game.draw_pieces_counter()
    game.draw_high_score()
    game.draw_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.save_high_score()
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
        draw_text(350, 0, "GAME OVER")

    pygame.display.update()
