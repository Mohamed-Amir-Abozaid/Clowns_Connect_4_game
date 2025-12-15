import numpy as np
import random
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
AI_DEPTH = 4

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

def get_valid_locations(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_location(board, c)]

def winning_move(board, piece):
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def is_draw(board):
    return len(get_valid_locations(board)) == 0 and \
           not winning_move(board, PLAYER_PIECE) and \
           not winning_move(board, AI_PIECE)

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or \
           winning_move(board, AI_PIECE) or \
           len(get_valid_locations(board)) == 0

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0
    center_array = list(board[:, COLUMN_COUNT//2])
    score += center_array.count(piece) * 3
    for r in range(ROW_COUNT):
        row_array = list(board[r,:])
        for c in range(COLUMN_COUNT-3):
            score += evaluate_window(row_array[c:c+4], piece)
    for c in range(COLUMN_COUNT):
        col_array = list(board[:,c])
        for r in range(ROW_COUNT-3):
            score += evaluate_window(col_array[r:r+4], piece)
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            score += evaluate_window([board[r+i][c+i] for i in range(4)], piece)
            score += evaluate_window([board[r+3-i][c+i] for i in range(4)], piece)
    return score

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return None, 10**14
            elif winning_move(board, PLAYER_PIECE):
                return None, -10**14
            else:
                return None, 0
        else:
            return None, score_position(board, AI_PIECE)
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE,
                (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK,
                (int(c*SQUARESIZE+SQUARESIZE/2),
                 int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED,
                    (int(c*SQUARESIZE+SQUARESIZE/2),
                     height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, YELLOW,
                    (int(c*SQUARESIZE+SQUARESIZE/2),
                     height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
def difficulty_menu():
    global AI_DEPTH
    choosing = True
    font = pygame.font.SysFont("arial", 50)
    buttons = [
        ("EASY", 1, pygame.Rect(200, 200, 300, 70)),
        ("MEDIUM", 3, pygame.Rect(200, 300, 300, 70)),
        ("HARD", 5, pygame.Rect(200, 400, 300, 70)),
    ]
    while choosing:
        screen.fill(BLACK)
        title = font.render("Choose Difficulty", True, YELLOW)
        screen.blit(title, (180, 100))
        for text, depth, rect in buttons:
            pygame.draw.rect(screen, BLUE, rect, border_radius=12)
            label = font.render(text, True, WHITE)
            screen.blit(
                label,
                (rect.centerx - label.get_width() // 2,
                 rect.centery - label.get_height() // 2)
            )
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for text, depth, rect in buttons:
                    if rect.collidepoint(event.pos):
                        AI_DEPTH = depth
                        choosing = False

pygame.init()
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
screen = pygame.display.set_mode((width, height))
RADIUS = int(SQUARESIZE/2 - 5)
myfont = pygame.font.SysFont("monospace", 75)

difficulty_menu()

board = create_board()
turn = random.randint(PLAYER, AI)
game_over = False
draw_board(board)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0,width,SQUARESIZE))
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (event.pos[0], SQUARESIZE//2), RADIUS)
            pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN and turn == PLAYER:
            col = event.pos[0] // SQUARESIZE
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, PLAYER_PIECE)
                if winning_move(board, PLAYER_PIECE):
                    screen.blit(myfont.render("Player Wins!", 1, RED), (40,10))
                    game_over = True
                elif is_draw(board):
                    screen.blit(myfont.render("Draw!", 1, BLUE), (40,10))
                    game_over = True
                draw_board(board)
                turn = AI

    if turn == AI and not game_over:
        col, _ = minimax(board, AI_DEPTH, -math.inf, math.inf, True)
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, AI_PIECE)
        if winning_move(board, AI_PIECE):
            screen.blit(myfont.render("AI Wins!", 1, YELLOW), (40,10))
            game_over = True
        elif is_draw(board):
            screen.blit(myfont.render("Draw!", 1, BLUE), (40,10))
            game_over = True
        draw_board(board)
        turn = PLAYER

    if game_over:
        pygame.time.wait(3000)
