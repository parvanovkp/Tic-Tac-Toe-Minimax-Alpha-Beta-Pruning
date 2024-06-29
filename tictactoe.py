import pygame
import sys
import time
import random
import math

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WIDTH, HEIGHT = 400, 450  # Increased height for difficulty slider
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)
TEXT_COLOR = (50, 205, 50)
MENU_COLOR = (100, 100, 100)
SLIDER_COLOR = (150, 150, 150)
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE

# Load sounds
try:
    X_SOUND = pygame.mixer.Sound("x_sound.wav")
    O_SOUND = pygame.mixer.Sound("o_sound.wav")
    WIN_SOUND = pygame.mixer.Sound("win_sound.wav")
    DRAW_SOUND = pygame.mixer.Sound("draw_sound.wav")
except pygame.error:
    print("Warning: Sound files not found. The game will run without sound effects.")
    X_SOUND = O_SOUND = WIN_SOUND = DRAW_SOUND = None

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Fonts
FONT = pygame.font.Font(None, 74)
MENU_FONT = pygame.font.Font(None, 36)

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False

def draw_board(game):
    screen.fill(BG_COLOR)
    
    # Draw grid lines
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 4)
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT-50), 4)
    
    # Draw X's and O's
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            pos = row * GRID_SIZE + col
            if game.board[pos] == 'X':
                draw_x(row, col)
            elif game.board[pos] == 'O':
                draw_o(row, col)

def draw_x(row, col):
    pygame.draw.line(screen, X_COLOR, 
                     (col * CELL_SIZE + 20, row * CELL_SIZE + 20),
                     ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20), 4)
    pygame.draw.line(screen, X_COLOR, 
                     ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20),
                     (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20), 4)

def draw_o(row, col):
    pygame.draw.circle(screen, O_COLOR, 
                       (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                       CELL_SIZE // 2 - 20, 4)

def play_sound(sound):
    if sound:
        sound.play()

def minimax(game, depth, alpha, beta, maximizing_player):
    if game.current_winner == 'O':
        return 1
    elif game.current_winner == 'X':
        return -1
    elif game.num_empty_squares() == 0:
        return 0

    if maximizing_player:
        max_eval = float('-inf')
        for move in game.available_moves():
            game.make_move(move, 'O')
            eval = minimax(game, depth + 1, alpha, beta, False)
            game.board[move] = ' '
            game.current_winner = None
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in game.available_moves():
            game.make_move(move, 'X')
            eval = minimax(game, depth + 1, alpha, beta, True)
            game.board[move] = ' '
            game.current_winner = None
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(game, difficulty):
    if random.random() > difficulty:
        return random.choice(game.available_moves())
    
    best_score = float('-inf')
    best_move = None
    for move in game.available_moves():
        game.make_move(move, 'O')
        score = minimax(game, 0, float('-inf'), float('inf'), False)
        game.board[move] = ' '
        game.current_winner = None
        if score > best_score:
            best_score = score
            best_move = move
    return best_move

def animate_text(text):
    text_surface = FONT.render(text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=(WIDTH/2, HEIGHT/2))
    
    for i in range(90):  # 3 seconds at 30 FPS
        alpha = int(255 * math.sin(i * math.pi / 180))  # Pulsating effect
        text_surface.set_alpha(alpha)
        
        screen.fill(BG_COLOR)
        draw_board(game)
        draw_difficulty_slider(difficulty)
        screen.blit(text_surface, text_rect)
        pygame.display.update()
        pygame.time.delay(33)  # Approximately 30 FPS

def draw_menu():
    screen.fill(BG_COLOR)
    title = FONT.render("Tic-Tac-Toe", True, TEXT_COLOR)
    screen.blit(title, (WIDTH/2 - title.get_width()/2, 50))

    options = ["Go First", "Go Second", "Coin Toss"]
    for i, option in enumerate(options):
        text = MENU_FONT.render(option, True, MENU_COLOR)
        text_rect = text.get_rect(center=(WIDTH/2, 200 + i * 60))
        pygame.draw.rect(screen, MENU_COLOR, text_rect.inflate(20, 10), 2)
        screen.blit(text, text_rect)

    pygame.display.update()

def get_menu_choice():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                for i in range(3):
                    button_rect = pygame.Rect(WIDTH/2 - 100, 190 + i * 60, 200, 40)
                    if button_rect.collidepoint(mouseX, mouseY):
                        return i  # 0 for Go First, 1 for Go Second, 2 for Coin Toss

def draw_difficulty_slider(difficulty):
    pygame.draw.rect(screen, SLIDER_COLOR, (20, HEIGHT - 40, WIDTH - 40, 20))
    slider_pos = int(20 + (WIDTH - 40) * difficulty)
    pygame.draw.rect(screen, TEXT_COLOR, (slider_pos - 5, HEIGHT - 45, 10, 30))
    
    text = MENU_FONT.render(f"AI Difficulty: {difficulty:.2f}", True, TEXT_COLOR)
    screen.blit(text, (20, HEIGHT - 70))

def handle_difficulty_slider(pos):
    if HEIGHT - 45 <= pos[1] <= HEIGHT - 15:
        return max(0, min(1, (pos[0] - 20) / (WIDTH - 40)))
    return None

def main():
    global game, difficulty
    game = TicTacToe()
    difficulty = 0.5  # Starting difficulty

    draw_menu()
    choice = get_menu_choice()

    if choice == 2:  # Coin Toss
        choice = random.randint(0, 1)

    player_turn = choice == 0
    game_over = False
    last_move_time = time.time()

    while True:
        current_time = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                new_difficulty = handle_difficulty_slider((mouseX, mouseY))
                if new_difficulty is not None:
                    difficulty = new_difficulty
                elif not game_over and player_turn and current_time - last_move_time > 0.5:
                    clicked_row = mouseY // CELL_SIZE
                    clicked_col = mouseX // CELL_SIZE
                    if clicked_row < 3:  # Ensure click is within the game board
                        if game.make_move(clicked_row * 3 + clicked_col, 'X'):
                            play_sound(X_SOUND)
                            player_turn = False
                            last_move_time = current_time
                            
                            if game.current_winner:
                                play_sound(WIN_SOUND)
                                animate_text("YOU WIN!")
                                game_over = True
                            elif game.num_empty_squares() == 0:
                                play_sound(DRAW_SOUND)
                                animate_text("DRAW!")
                                game_over = True
        
        if not player_turn and not game_over and current_time - last_move_time > 0.5:
            ai_move = get_best_move(game, difficulty)
            game.make_move(ai_move, 'O')
            play_sound(O_SOUND)
            player_turn = True
            last_move_time = current_time
            
            if game.current_winner:
                play_sound(WIN_SOUND)
                animate_text("YOU LOSE!")
                game_over = True
            elif game.num_empty_squares() == 0:
                play_sound(DRAW_SOUND)
                animate_text("DRAW!")
                game_over = True

        draw_board(game)
        draw_difficulty_slider(difficulty)
        pygame.display.update()

        if game_over and current_time - last_move_time > 3:
            game = TicTacToe()
            game_over = False
            draw_menu()
            choice = get_menu_choice()
            if choice == 2:  # Coin Toss
                choice = random.randint(0, 1)
            player_turn = choice == 0
            last_move_time = time.time()

if __name__ == "__main__":
    main()