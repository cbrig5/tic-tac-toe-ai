import pygame
from game.game import TicTacToe

pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 5
BOARD_ROWS = 3
BOARD_COLS = 3
CELL_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = CELL_SIZE // 4

# Colors
BG_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0) 
CIRCLE_COLOR = (0, 0, 0)
CROSS_COLOR = (255, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(BG_COLOR)

# Game object
game = TicTacToe()

def draw_lines():
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            index = row * 3 + col
            if game.board[index] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                                   CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif game.board[index] == 'X':
                start_desc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + SPACE)
                end_desc = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + CELL_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

                start_asc = (col * CELL_SIZE + SPACE, row * CELL_SIZE + CELL_SIZE - SPACE)
                end_asc = (col * CELL_SIZE + CELL_SIZE - SPACE, row * CELL_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

def restart_game():
    screen.fill(BG_COLOR)
    draw_lines()
    game.reset()

def show_winner(winner):
    pygame.draw.rect(screen, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    font = pygame.font.Font(None, 74)

    if winner == 'X':
        text = font.render("X wins!", True, (255, 255, 255))
    elif winner == 'O':
        text = font.render("O wins!", True, (255, 255, 255))
    else:
        text = font.render("It's a draw!", True, (255, 255, 255))

    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.update()

    # Restart button
    restart_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), restart_button)
    restart_text = font.render("Restart", True, (255, 255, 255))
    text_rect = restart_text.get_rect(center=restart_button.center)
    screen.blit(restart_text, text_rect)
    pygame.display.update()

    # Quit button
    quit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 120, 200, 50)
    pygame.draw.rect(screen, (255, 0, 0), quit_button)
    quit_text = font.render("Quit", True, (255, 255, 255))
    text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, text_rect)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    restart_game()
                    return
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

draw_lines()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = mouseY // CELL_SIZE
            clicked_col = mouseX // CELL_SIZE
            index = clicked_row * BOARD_COLS + clicked_col

            if game.board[index] == '' and game.check_winner() is None:
                game.make_move(index)
                draw_figures()

                winner = game.check_winner()
                if winner:
                    show_winner(winner)
                    game_over = True
                    print(f"Winner: {winner}")

    draw_figures()
    pygame.display.update()
