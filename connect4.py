import numpy as np
import pygame
import sys
import math

# ================= COLORS =================
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)

# ================= CONSTANTS =================
ROW_COUNT = 6
COLUMN_COUNT = 7

# ================= BOARD FUNCTIONS =================
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Horizontal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True

    # Vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True

    # Positive diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True

    # Negative diagonal
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True

    return False

def is_draw(board):
    for c in range(COLUMN_COUNT):
        if is_valid_location(board, c):
            return False
    return True

# ================= DRAW BOARD =================
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen, BLUE,
                (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE)
            )
            pygame.draw.circle(
                screen, BLACK,
                (int(c*SQUARESIZE + SQUARESIZE/2),
                 int(r*SQUARESIZE + SQUARESIZE + SQUARESIZE/2)),
                RADIUS
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(
                    screen, RED,
                    (int(c*SQUARESIZE + SQUARESIZE/2),
                     height - int(r*SQUARESIZE + SQUARESIZE/2)),
                    RADIUS
                )
            elif board[r][c] == 2:
                pygame.draw.circle(
                    screen, YELLOW,
                    (int(c*SQUARESIZE + SQUARESIZE/2),
                     height - int(r*SQUARESIZE + SQUARESIZE/2)),
                    RADIUS
                )

    pygame.display.update()

# ================= MAIN =================
board = create_board()
game_over = False
turn = 0  # 0 -> Player 1 , 1 -> Player 2

pygame.init()

SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4 - Player vs Player")

RADIUS = int(SQUARESIZE/2 - 5)
myfont = pygame.font.SysFont("monospace", 60)

draw_board(board)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
            posx = event.pos[0]
            color = RED if turn == 0 else YELLOW
            pygame.draw.circle(screen, color, (posx, SQUARESIZE//2), RADIUS)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

            posx = event.pos[0]
            col = int(posx // SQUARESIZE)

            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                piece = 1 if turn == 0 else 2
                drop_piece(board, row, col, piece)

                if winning_move(board, piece):
                    text = f"Player {piece} Wins!"
                    color = RED if piece == 1 else YELLOW
                    label = myfont.render(text, True, color)
                    screen.blit(label, (40, 10))
                    game_over = True

                elif is_draw(board):
                    label = myfont.render("DRAW!", True, WHITE)
                    screen.blit(label, (200, 10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn = (turn + 1) % 2

    if game_over:
        pygame.time.wait(3000)
