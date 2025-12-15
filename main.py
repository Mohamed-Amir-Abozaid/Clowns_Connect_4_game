import pygame
import sys
import subprocess
import os

WHITE = (255, 255, 255)
BG_COLOR = (12, 12, 18)

ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4 Menu")

font_title = pygame.font.SysFont("arialblack", 60)
font_btn = pygame.font.SysFont("arial", 34)
font_small = pygame.font.SysFont("arial", 22)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def game_mode_menu():
    clock = pygame.time.Clock()

    buttons = [
        {"text": "PLAYER vs PLAYER", "file": "connect4.py"},
        {"text": "PLAYER vs AI", "file": "connect4_with_ai.py"},
        {"text": "AI vs AI", "file": "connect4_ai_vs_ai.py"}
    ]

    rects = [
        pygame.Rect(width // 2 - 240, 280 + i * 90, 480, 70)
        for i in range(len(buttons))
    ]

    pulse = 0
    direction = 1
    game_process = None

    while True:
        clock.tick(60)
        screen.fill(BG_COLOR)

        if game_process and game_process.poll() is not None:
            game_process = None

        pulse += direction
        if pulse > 20 or pulse < 0:
            direction *= -1

        title = font_title.render("CONNECT 4", True, (255, 215, 0))
        screen.blit(title, (width // 2 - title.get_width() // 2, 75))

        subtitle = font_btn.render("Choose Game Mode", True, (180, 180, 180))
        screen.blit(subtitle, (width // 2 - subtitle.get_width() // 2, 200))

        footer = font_small.render("Menu stays open", True, (120, 120, 120))
        screen.blit(footer, (width // 2 - footer.get_width() // 2, height - 40))

        mouse_pos = pygame.mouse.get_pos()
        for i, btn in enumerate(buttons):
            color = (90, 150, 255) if rects[i].collidepoint(mouse_pos) else (40, 70, 140)
            pygame.draw.rect(screen, color, rects[i], border_radius=18)
            pygame.draw.rect(screen, WHITE, rects[i], 2, border_radius=18)

            label = font_btn.render(btn["text"], True, WHITE)
            screen.blit(
                label,
                (rects[i].centerx - label.get_width() // 2,
                 rects[i].centery - label.get_height() // 2)
            )

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if game_process:
                    game_process.terminate()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, btn in enumerate(buttons):
                    if rects[i].collidepoint(event.pos):
                        if game_process is None:
                            file_path = os.path.join(BASE_DIR, btn["file"])
                            game_process = subprocess.Popen(
                                [sys.executable, file_path]
                            )

game_mode_menu()
