import pygame
import sys
import random
import time
import os
import json  # For saving scores and leaderboard data

"""
Program Name: Tic-Tac-Toe with AI and Enhanced Features
Author: [Jeremiah Ddumba]
Email: [jsd5521@psu.edu]
Extra Credit 
Assignment: Final Project - Tic-Tac-Toe with Difficulty Levels and Enhancements
Due Date: [11/23/2024]
File Name: tic_tac_toe_ai_scoring_pygame.py
Program Purpose: Play Tic-Tac-Toe with various game modes, AI difficulty levels, track detailed statistics, and enhanced user experience with sounds and animations, including a dark mode.
Compiler: Python 3.12
Operating System: [MacOS Sonoma, Windows, Linux]
References:
- Python Documentation: https://docs.python.org/3/
- Pygame Documentation: https://www.pygame.org/docs/
"""

# Initialize pygame and mixer for sound effects
pygame.init()
pygame.mixer.init()

# Set up the game window
WINDOW_SIZE = 600  # Starting size
WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
pygame.display.set_caption('Tic-Tac-Toe')

# Define color schemes
LIGHT_THEME = {
    'background': (255, 255, 255),
    'grid': (0, 0, 0),
    'text': (0, 0, 0),
    'highlight': (144, 238, 144),
    'button': (211, 211, 211),
    'button_text': (0, 0, 0),
    'input_box_active': (255, 255, 0),
}

DARK_THEME = {
    'background': (34, 34, 34),
    'grid': (255, 255, 255),
    'text': (255, 255, 255),
    'highlight': (70, 130, 180),
    'button': (105, 105, 105),
    'button_text': (255, 255, 255),
    'input_box_active': (255, 215, 0),
}

# Define fonts
FONT = pygame.font.SysFont('Arial', 24)
SCORE_FONT = pygame.font.SysFont('Arial', 16)
STATS_FONT = pygame.font.SysFont('Arial', 12)

# Define game states
MENU = 'menu'
GAME = 'game'
SETTINGS = 'settings'
PAUSE = 'pause'
GAME_OVER = 'game_over'  # State for game over screen
LEADERBOARD = 'leaderboard'  # State for leaderboard screen

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (0, 0, 0)  # Default color before theme is applied
        self.color_active = (255, 255, 0)  # Default active color before theme
        self.color = self.color_inactive
        self.text = text
        self.active = False
        self.txt_surface = FONT.render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        elif event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text.strip()
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)
        return None

    def draw(self, surface):
        # Blit the text
        surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect
        pygame.draw.rect(surface, self.color, self.rect, 2)

    def update_theme(self, theme):
        self.color_inactive = theme['text']
        self.color_active = theme['input_box_active']
        self.color = self.color_active if self.active else self.color_inactive
        self.txt_surface = FONT.render(self.text, True, self.color)

class TicTacToe:
    def __init__(self):
        # Initialize game variables
        self.current_player = 'X'  # Player always starts as 'X'
        self.board = [''] * 9  # 3x3 board
        self.player_score = 0
        self.ai_score = 0
        self.player_wins = 0
        self.ai_wins = 0
        self.ties = 0
        self.total_games = 0
        self.difficulty = 'Easy'  # Default difficulty
        self.player_name = 'Player'
        self.ai_name = 'AI'
        self.game_mode = 'Player vs AI'  # Default game mode
        self.ai_depth = 9  # Default depth for AI (for minimax)
        self.ai_personality = 'Balanced'  # Default AI personality
        self.animation_speed = 100  # milliseconds
        self.running = True
        self.cell_size = WINDOW_SIZE // 3
        self.grid_lines = [
            # Vertical lines
            ((self.cell_size, 0), (self.cell_size, WINDOW_SIZE)),
            ((2 * self.cell_size, 0), (2 * self.cell_size, WINDOW_SIZE)),
            # Horizontal lines
            ((0, self.cell_size), (WINDOW_SIZE, self.cell_size)),
            ((0, 2 * self.cell_size), (WINDOW_SIZE, 2 * self.cell_size))
        ]
        self.last_move = None  # Track the last move index
        self.state = MENU  # Start in the main menu
        self.previous_state = None  # Track previous state
        self.input_box = InputBox(200, 150, 200, 40)  # Adjusted position
        self.input_active = False
        self.clock = pygame.time.Clock()
        self.FPS = 60  # Frames per second
        self.back_button_rect = pygame.Rect(10, 10, 80, 30)
        self.save_file = 'scores.json'  # File to save scores
        self.leaderboard_file = 'leaderboard.json'  # File to save leaderboard
        self.leaderboard = {}  # Initialize leaderboard
        self.theme_file = 'theme.json'  # File to save theme preference
        self.theme = 'Light'  # Default theme
        self.themes = {'Light': LIGHT_THEME, 'Dark': DARK_THEME}

        # For scrolling in settings
        self.settings_scroll_offset = 0  # Scroll offset for settings screen
        self.content_height = 0  # Total height of the settings content
        # Initialize clickable areas list
        self.settings_clickable_areas = []

        # Load configurations
        self.load_scores()       # Load scores at startup
        self.load_leaderboard()  # Load leaderboard at startup
        self.load_theme()        # Load theme preference
        self.update_theme()      # Apply the theme to UI elements

        # Initialize the game
        self.main_loop()

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_scores()  # Save scores on exit
                self.save_leaderboard()  # Save leaderboard on exit
                self.save_theme()  # Save theme preference
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.handle_window_resize(event.w, event.h)
            if self.state == MENU:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_menu_click(event.pos)
            elif self.state == GAME:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)
                    self.handle_back_button(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = PAUSE
                    elif event.key == pygame.K_e:
                        self.set_difficulty('Easy')
                    elif event.key == pygame.K_m:
                        self.set_difficulty('Medium')
                    elif event.key == pygame.K_h:
                        self.set_difficulty('Hard')
                    elif event.key == pygame.K_r:
                        self.reset_board()
                    elif event.key == pygame.K_ESCAPE:
                        self.state = MENU
            elif self.state == PAUSE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = GAME
                    elif event.key == pygame.K_ESCAPE:
                        self.state = MENU
            elif self.state == SETTINGS:
                result = self.input_box.handle_event(event)
                if result is not None and result != '':
                    self.player_name = result
                    self.input_active = False
                    # Show message after initialization
                    self.show_message(f"Player name set to {self.player_name}")
                    # Update state based on previous state
                    if self.previous_state == GAME_OVER:
                        self.reset_board()
                        self.state = GAME  # Start a new game
                    else:
                        self.state = MENU
                elif result == '':
                    self.show_message("Name cannot be empty!")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:  # Mouse wheel up
                        self.settings_scroll_offset += 20  # Adjust the scroll speed as needed
                        if self.settings_scroll_offset > 0:
                            self.settings_scroll_offset = 0  # Prevent scrolling above the content
                    elif event.button == 5:  # Mouse wheel down
                        max_scroll = min(0, WINDOW_SIZE - self.content_height)
                        self.settings_scroll_offset -= 20  # Adjust the scroll speed as needed
                        if self.settings_scroll_offset < max_scroll:
                            self.settings_scroll_offset = max_scroll  # Prevent scrolling beyond the content
                    else:
                        adjusted_pos = (event.pos[0], event.pos[1] - self.settings_scroll_offset)
                        self.handle_settings_click(adjusted_pos)
            elif self.state == GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_game_over_click(event.pos)
            elif self.state == 'select_mode':
                if event.type == pygame.KEYDOWN:
                    # Handle key presses for selecting mode and difficulty
                    if event.key == pygame.K_1:
                        self.set_game_mode('Player vs AI')
                        self.state = MENU
                    elif event.key == pygame.K_2:
                        self.set_game_mode('Player vs Player')
                        self.state = MENU
                    elif event.key == pygame.K_3:
                        self.set_game_mode('AI vs AI')
                        self.state = MENU
                    elif event.key == pygame.K_e:
                        self.set_difficulty('Easy')
                        self.state = MENU
                    elif event.key == pygame.K_m:
                        self.set_difficulty('Medium')
                        self.state = MENU
                    elif event.key == pygame.K_h:
                        self.set_difficulty('Hard')
                        self.state = MENU
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_select_mode_click(event.pos)
            elif self.state == LEADERBOARD:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_leaderboard_click(event.pos)

    def handle_window_resize(self, width, height):
        global WINDOW_SIZE, WINDOW
        WINDOW_SIZE = min(width, height)  # Keep the window square
        if WINDOW_SIZE < 300:
            WINDOW_SIZE = 300  # Set a minimum size
        WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
        self.cell_size = WINDOW_SIZE // 3
        # Recalculate grid lines
        self.grid_lines = [
            # Vertical lines
            ((self.cell_size, 0), (self.cell_size, WINDOW_SIZE)),
            ((2 * self.cell_size, 0), (2 * self.cell_size, WINDOW_SIZE)),
            # Horizontal lines
            ((0, self.cell_size), (WINDOW_SIZE, self.cell_size)),
            ((0, 2 * self.cell_size), (WINDOW_SIZE, 2 * self.cell_size))
        ]

    def handle_back_button(self, pos):
        if self.back_button_rect.collidepoint(pos):
            self.state = MENU

    def handle_menu_click(self, pos):
        x, y = pos
        button_width = WINDOW_SIZE * 0.4
        button_height = WINDOW_SIZE * 0.08
        button_x = WINDOW_SIZE // 2 - button_width // 2

        # Play button area
        if button_x <= x <= button_x + button_width and WINDOW_SIZE * 0.3 <= y <= WINDOW_SIZE * 0.3 + button_height:
            self.state = GAME
            self.reset_board()
        elif button_x <= x <= button_x + button_width and WINDOW_SIZE * 0.4 <= y <= WINDOW_SIZE * 0.4 + button_height:
            self.previous_state = MENU  # Track where settings was accessed from
            self.state = SETTINGS
        elif button_x <= x <= button_x + button_width and WINDOW_SIZE * 0.5 <= y <= WINDOW_SIZE * 0.5 + button_height:
            self.state = LEADERBOARD  # Go to leaderboard screen
        elif button_x <= x <= button_x + button_width and WINDOW_SIZE * 0.6 <= y <= WINDOW_SIZE * 0.6 + button_height:
            self.running = False
            self.save_scores()  # Save scores on exit
            self.save_leaderboard()  # Save leaderboard on exit
            self.save_theme()  # Save theme preference
            pygame.quit()
            sys.exit()

    def handle_settings_click(self, pos):
        # Handle back button click (do not adjust for scroll offset)
        self.handle_back_button(pos)
        # Adjust y position for scroll offset
        pos = (pos[0], pos[1] + self.settings_scroll_offset)
        # Check if click is within any clickable area
        for action, value, rect in self.settings_clickable_areas:
            if rect.collidepoint(pos):
                if action == 'set_difficulty':
                    self.set_difficulty(value)
                elif action == 'set_game_mode':
                    self.set_game_mode(value)
                elif action == 'toggle_theme':
                    self.toggle_theme()
                elif action == 'set_ai_personality':
                    self.set_ai_personality(value)
                # Start a new game if coming from GAME_OVER
                if self.previous_state == GAME_OVER:
                    self.reset_board()
                    self.state = GAME
                break  # Stop checking after first match

    def handle_select_mode_click(self, pos):
        x, y = pos
        # Handle game mode selection
        if 200 <= x <= 400:
            if 190 <= y <= 220:
                self.set_game_mode('Player vs AI')
            elif 230 <= y <= 260:
                self.set_game_mode('Player vs Player')
            elif 270 <= y <= 300:
                self.set_game_mode('AI vs AI')
            # Handle difficulty selection
            elif 370 <= y <= 400:
                self.set_difficulty('Easy')
            elif 410 <= y <= 440:
                self.set_difficulty('Medium')
            elif 450 <= y <= 480:
                self.set_difficulty('Hard')
        self.state = MENU  # Return to menu after selection

    def handle_game_over_click(self, pos):
        # Buttons on the game over screen
        if 200 <= pos[0] <= 400:
            if 250 <= pos[1] <= 290:
                self.reset_board()
                self.state = GAME
            elif 300 <= pos[1] <= 340:
                self.previous_state = GAME_OVER  # Track previous state
                self.state = SETTINGS
            elif 350 <= pos[1] <= 390:
                self.state = MENU

    def handle_leaderboard_click(self, pos):
        # Handle back button click
        self.handle_back_button(pos)

    def handle_click(self, pos):
        x, y = pos
        row = y // self.cell_size
        col = x // self.cell_size
        index = row * 3 + col
        if 0 <= index < 9 and self.board[index] == '':
            self.make_move(index)
        # Handle back button click
        self.handle_back_button(pos)

    def make_move(self, index):
        if self.board[index] == '':
            self.board[index] = self.current_player
            self.last_move = index
            if self.check_winner(self.board, self.current_player):
                self.handle_win(self.current_player)
            elif '' not in self.board:
                self.handle_tie()
            else:
                self.switch_turns()
                if self.game_mode == 'Player vs AI' and self.current_player == 'O':
                    self.ai_move()
                elif self.game_mode == 'AI vs AI':
                    self.ai_move()
                elif self.game_mode == 'Player vs Player':
                    pass  # Do nothing, wait for the next player's move

    def switch_player(self, player):
        """Switch the player."""
        return 'O' if player == 'X' else 'X'

    def switch_turns(self):
        """Switch the current player for the actual game."""
        self.current_player = self.switch_player(self.current_player)

    def ai_move(self):
        pygame.time.wait(self.animation_speed)
        empty_indices = [i for i, x in enumerate(self.board) if x == '']
        if not empty_indices:
            return

        if self.difficulty == 'Easy':
            index = random.choice(empty_indices)
        elif self.difficulty == 'Medium':
            index = self.block_player(empty_indices)
        else:
            if self.ai_personality == 'Aggressive':
                index = self.aggressive_move(empty_indices)
            elif self.ai_personality == 'Defensive':
                index = self.defensive_move(empty_indices)
            else:  # Balanced
                index = self.minimax_ai()
        self.make_move(index)
        if self.game_mode == 'AI vs AI':
            pygame.time.wait(500)  # Adjust delay as needed

    def aggressive_move(self, empty_indices):
        # Try to win first
        for index in empty_indices:
            self.board[index] = self.current_player
            if self.check_winner(self.board, self.current_player):
                self.board[index] = ''
                return index
            self.board[index] = ''
        # If can't win, make a random move
        return random.choice(empty_indices)

    def defensive_move(self, empty_indices):
        # Try to block opponent first
        opponent = self.switch_player(self.current_player)
        for index in empty_indices:
            self.board[index] = opponent
            if self.check_winner(self.board, opponent):
                self.board[index] = ''
                return index
            self.board[index] = ''
        # If no block needed, make a random move
        return random.choice(empty_indices)

    def block_player(self, empty_indices):
        # Try to win
        for index in empty_indices:
            self.board[index] = self.current_player
            if self.check_winner(self.board, self.current_player):
                self.board[index] = ''
                return index
            self.board[index] = ''
        # Try to block opponent
        opponent = self.switch_player(self.current_player)
        for index in empty_indices:
            self.board[index] = opponent
            if self.check_winner(self.board, opponent):
                self.board[index] = ''
                return index
            self.board[index] = ''
        # Pick center or random
        if 4 in empty_indices:
            return 4
        return random.choice(empty_indices)

    def minimax_ai(self):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == '':
                self.board[i] = self.current_player
                score = self.minimax(self.board, self.switch_player(self.current_player), False)
                self.board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, player, is_maximizing, alpha=-float('inf'), beta=float('inf')):
        opponent = self.switch_player(player)
        if self.check_winner(board, opponent):
            return 1 if opponent == self.current_player else -1
        elif '' not in board:
            return 0

        if is_maximizing:
            max_eval = -float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = player
                    eval = self.minimax(board, self.switch_player(player), False, alpha, beta)
                    board[i] = ''
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(9):
                if board[i] == '':
                    board[i] = player
                    eval = self.minimax(board, self.switch_player(player), True, alpha, beta)
                    board[i] = ''
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def check_winner(self, board, player):
        win_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6],
        ]
        for combo in win_combinations:
            if all(board[i] == player for i in combo):
                self.draw_winning_line(combo)
                return True
        return False

    def draw_winning_line(self, combo):
        # Draw a line over the winning combination with animation
        start_index = combo[0]
        end_index = combo[2]
        start_pos = ((start_index % 3) * self.cell_size + self.cell_size // 2,
                     (start_index // 3) * self.cell_size + self.cell_size // 2)
        end_pos = ((end_index % 3) * self.cell_size + self.cell_size // 2,
                   (end_index // 3) * self.cell_size + self.cell_size // 2)
        for i in range(5):
            pygame.draw.line(WINDOW, self.themes[self.theme]['highlight'], start_pos, end_pos, i)
            pygame.display.update()
            pygame.time.wait(100)

    def handle_win(self, winner):
        self.total_games += 1
        if winner == 'X':
            self.player_score += 1
            self.player_wins += 1
            message = f"{self.player_name} wins!"
            # Update leaderboard
            self.update_leaderboard()
        else:
            self.ai_score += 1
            self.ai_wins += 1
            message = f"{self.ai_name} wins!"
        self.save_scores()  # Save scores when a game ends
        # Show message
        self.show_message(message)
        # Move to game over state
        self.state = GAME_OVER

    def handle_tie(self):
        self.ties += 1
        self.total_games += 1
        self.save_scores()  # Save scores when a game ends
        self.show_message("It's a tie!")
        # Move to game over state
        self.state = GAME_OVER

    def show_message(self, message):
        # Display message in the center of the screen
        text_surface = FONT.render(message, True, self.themes[self.theme]['text'])
        rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        WINDOW.blit(text_surface, rect)
        pygame.display.update()
        pygame.time.wait(2000)

    def reset_board(self):
        self.board = [''] * 9
        self.current_player = 'X'
        self.last_move = None
        # If AI vs AI, start AI move
        if self.game_mode == 'AI vs AI':
            self.ai_move()

    def draw(self):
        if self.state == MENU:
            self.draw_menu()
        elif self.state == GAME:
            self.draw_game()
        elif self.state == SETTINGS:
            self.draw_settings()
        elif self.state == PAUSE:
            self.draw_pause_menu()
        elif self.state == GAME_OVER:
            self.draw_game_over()
        elif self.state == 'select_mode':
            self.draw_select_mode()
        elif self.state == LEADERBOARD:
            self.draw_leaderboard()

    def draw_menu(self):
        WINDOW.fill(self.themes[self.theme]['background'])
        title = FONT.render("Tic-Tac-Toe", True, self.themes[self.theme]['text'])
        WINDOW.blit(title, (WINDOW_SIZE // 2 - title.get_width() // 2, WINDOW_SIZE * 0.1))

        # Calculate button positions dynamically
        button_width = WINDOW_SIZE * 0.4
        button_height = WINDOW_SIZE * 0.08
        button_x = WINDOW_SIZE // 2 - button_width // 2

        # Play button
        play_button_rect = pygame.Rect(button_x, WINDOW_SIZE * 0.3, button_width, button_height)
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], play_button_rect)
        play_text = FONT.render("Play", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(play_text, (play_button_rect.x + play_button_rect.width // 2 - play_text.get_width() // 2,
                                play_button_rect.y + play_button_rect.height // 2 - play_text.get_height() // 2))

        # Settings button
        settings_button_rect = pygame.Rect(button_x, WINDOW_SIZE * 0.4, button_width, button_height)
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], settings_button_rect)
        settings_text = FONT.render("Settings", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(settings_text, (settings_button_rect.x + settings_button_rect.width // 2 - settings_text.get_width() // 2,
                                    settings_button_rect.y + settings_button_rect.height // 2 - settings_text.get_height() // 2))

        # Leaderboard button
        leaderboard_button_rect = pygame.Rect(button_x, WINDOW_SIZE * 0.5, button_width, button_height)
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], leaderboard_button_rect)
        leaderboard_text = FONT.render("Leaderboard", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(leaderboard_text, (leaderboard_button_rect.x + leaderboard_button_rect.width // 2 - leaderboard_text.get_width() // 2,
                                       leaderboard_button_rect.y + leaderboard_button_rect.height // 2 - leaderboard_text.get_height() // 2))

        # Exit button
        exit_button_rect = pygame.Rect(button_x, WINDOW_SIZE * 0.6, button_width, button_height)
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], exit_button_rect)
        exit_text = FONT.render("Exit", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(exit_text, (exit_button_rect.x + exit_button_rect.width // 2 - exit_text.get_width() // 2,
                                exit_button_rect.y + exit_button_rect.height // 2 - exit_text.get_height() // 2))

    def draw_game(self):
        # Fill the screen with background color
        WINDOW.fill(self.themes[self.theme]['background'])
        # Draw grid lines
        for line in self.grid_lines:
            pygame.draw.line(WINDOW, self.themes[self.theme]['grid'], line[0], line[1], 2)
        # Highlight last move
        if self.last_move is not None:
            x = (self.last_move % 3) * self.cell_size
            y = (self.last_move // 3) * self.cell_size
            highlight_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(WINDOW, self.themes[self.theme]['highlight'], highlight_rect)
        # Draw Xs and Os
        for i in range(9):
            x = (i % 3) * self.cell_size
            y = (i // 3) * self.cell_size
            if self.board[i] == 'X':
                self.draw_x(x, y)
            elif self.board[i] == 'O':
                self.draw_o(x, y)
        # Draw scores and stats
        self.draw_scores()
        self.draw_stats()
        # Draw Back Button
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], self.back_button_rect)
        back_text = SCORE_FONT.render("Back", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5))

    def draw_x(self, x, y):
        # Draw an X at the given position
        padding = self.cell_size // 4
        start_pos = (x + padding, y + padding)
        end_pos = (x + self.cell_size - padding, y + self.cell_size - padding)
        pygame.draw.line(WINDOW, self.themes[self.theme]['text'], start_pos, end_pos, 5)
        start_pos = (x + self.cell_size - padding, y + padding)
        end_pos = (x + padding, y + self.cell_size - padding)
        pygame.draw.line(WINDOW, self.themes[self.theme]['text'], start_pos, end_pos, 5)

    def draw_o(self, x, y):
        # Draw an O at the given position
        center = (x + self.cell_size // 2, y + self.cell_size // 2)
        radius = self.cell_size // 2 - self.cell_size // 4
        pygame.draw.circle(WINDOW, self.themes[self.theme]['text'], center, radius, 5)

    def draw_scores(self):
        # Draw the scores on the screen
        score_text = SCORE_FONT.render(f"{self.player_name}: {self.player_score}    {self.ai_name}: {self.ai_score}", True, self.themes[self.theme]['text'])
        WINDOW.blit(score_text, (WINDOW_SIZE // 2 - score_text.get_width() // 2, 10))

    def draw_stats(self):
        # Draw game statistics
        stats_text = STATS_FONT.render(f"Total Games: {self.total_games}    Wins: {self.player_wins}    Losses: {self.ai_wins}    Ties: {self.ties}", True, self.themes[self.theme]['text'])
        WINDOW.blit(stats_text, (WINDOW_SIZE // 2 - stats_text.get_width() // 2, 30))

    def draw_settings(self):
        WINDOW.fill(self.themes[self.theme]['background'])
        y_offset = 50 + self.settings_scroll_offset  # Start position for the first element

        # Initialize the list of clickable areas
        self.settings_clickable_areas = []

        title = FONT.render("Settings", True, self.themes[self.theme]['text'])
        WINDOW.blit(title, (WINDOW_SIZE//2 - title.get_width()//2, y_offset))
        y_offset += 60  # Adjust spacing

        name_label = FONT.render("Enter your name:", True, self.themes[self.theme]['text'])
        WINDOW.blit(name_label, (WINDOW_SIZE//2 - name_label.get_width()//2, y_offset))
        y_offset += 40  # Adjust spacing

        # Adjust input box position
        self.input_box.rect.y = y_offset
        self.input_box.draw(WINDOW)
        y_offset += self.input_box.rect.height + 20  # Adjust spacing

        # Difficulty selection
        difficulty_label = FONT.render("Select Difficulty:", True, self.themes[self.theme]['text'])
        WINDOW.blit(difficulty_label, (WINDOW_SIZE//2 - difficulty_label.get_width()//2, y_offset))
        y_offset += 30  # Adjust spacing

        # "Easy" button
        easy_button = SCORE_FONT.render("Easy", True, self.themes[self.theme]['text'])
        easy_button_rect = easy_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_difficulty', 'Easy', easy_button_rect))
        WINDOW.blit(easy_button, easy_button_rect)
        y_offset += 40  # Adjust spacing

        # "Medium" button
        medium_button = SCORE_FONT.render("Medium", True, self.themes[self.theme]['text'])
        medium_button_rect = medium_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_difficulty', 'Medium', medium_button_rect))
        WINDOW.blit(medium_button, medium_button_rect)
        y_offset += 40  # Adjust spacing

        # "Hard" button
        hard_button = SCORE_FONT.render("Hard", True, self.themes[self.theme]['text'])
        hard_button_rect = hard_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_difficulty', 'Hard', hard_button_rect))
        WINDOW.blit(hard_button, hard_button_rect)
        y_offset += 60  # Adjust spacing

        # Game mode selection
        mode_label = FONT.render("Select Game Mode:", True, self.themes[self.theme]['text'])
        WINDOW.blit(mode_label, (WINDOW_SIZE//2 - mode_label.get_width()//2, y_offset))
        y_offset += 30  # Adjust spacing

        # "Player vs AI" button
        p_vs_ai_button = SCORE_FONT.render("Player vs AI", True, self.themes[self.theme]['text'])
        p_vs_ai_button_rect = p_vs_ai_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_game_mode', 'Player vs AI', p_vs_ai_button_rect))
        WINDOW.blit(p_vs_ai_button, p_vs_ai_button_rect)
        y_offset += 40  # Adjust spacing

        # "Player vs Player" button
        p_vs_p_button = SCORE_FONT.render("Player vs Player", True, self.themes[self.theme]['text'])
        p_vs_p_button_rect = p_vs_p_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_game_mode', 'Player vs Player', p_vs_p_button_rect))
        WINDOW.blit(p_vs_p_button, p_vs_p_button_rect)
        y_offset += 40  # Adjust spacing

        # "AI vs AI" button
        ai_vs_ai_button = SCORE_FONT.render("AI vs AI", True, self.themes[self.theme]['text'])
        ai_vs_ai_button_rect = ai_vs_ai_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_game_mode', 'AI vs AI', ai_vs_ai_button_rect))
        WINDOW.blit(ai_vs_ai_button, ai_vs_ai_button_rect)
        y_offset += 60  # Adjust spacing

        # Theme toggle
        theme_button = SCORE_FONT.render(f"Toggle Theme (Current: {self.theme})", True, self.themes[self.theme]['text'])
        theme_button_rect = theme_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('toggle_theme', None, theme_button_rect))
        WINDOW.blit(theme_button, theme_button_rect)
        y_offset += 40  # Adjust spacing

        # AI Personality selection
        personality_label = FONT.render("Select AI Personality:", True, self.themes[self.theme]['text'])
        WINDOW.blit(personality_label, (WINDOW_SIZE//2 - personality_label.get_width()//2, y_offset))
        y_offset += 30  # Adjust spacing

        # "Aggressive" button
        aggressive_button = SCORE_FONT.render("Aggressive", True, self.themes[self.theme]['text'])
        aggressive_button_rect = aggressive_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_ai_personality', 'Aggressive', aggressive_button_rect))
        WINDOW.blit(aggressive_button, aggressive_button_rect)
        y_offset += 40  # Adjust spacing

        # "Defensive" button
        defensive_button = SCORE_FONT.render("Defensive", True, self.themes[self.theme]['text'])
        defensive_button_rect = defensive_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_ai_personality', 'Defensive', defensive_button_rect))
        WINDOW.blit(defensive_button, defensive_button_rect)
        y_offset += 40  # Adjust spacing

        # "Balanced" button
        balanced_button = SCORE_FONT.render("Balanced", True, self.themes[self.theme]['text'])
        balanced_button_rect = balanced_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_ai_personality', 'Balanced', balanced_button_rect))
        WINDOW.blit(balanced_button, balanced_button_rect)
        y_offset += 40  # Adjust spacing

        # Update content height
        self.content_height = y_offset - self.settings_scroll_offset

        # Draw Back Button (do not adjust for scroll offset)
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], self.back_button_rect)
        back_text = SCORE_FONT.render("Back", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5))

    def draw_game_over(self):
        # Implement the game over screen drawing
        WINDOW.fill(self.themes[self.theme]['background'])
        message = FONT.render("Game Over!", True, self.themes[self.theme]['text'])
        WINDOW.blit(message, (WINDOW_SIZE // 2 - message.get_width() // 2, WINDOW_SIZE * 0.2))

        # Buttons for "Play Again", "Settings", "Main Menu"
        button_width = 200
        button_height = 40
        button_x = WINDOW_SIZE // 2 - button_width // 2

        # "Play Again" button
        play_again_rect = pygame.Rect(button_x, 250, button_width, button_height)
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], play_again_rect)
        play_again_text = SCORE_FONT.render("Play Again", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(play_again_text, (play_again_rect.x + play_again_rect.width // 2 - play_again_text.get_width() // 2,
                                      play_again_rect.y + play_again_rect.height // 2 - play_again_text.get_height() // 2))

        # "Settings" button
        settings_rect = pygame.Rect(button_x, 300, button_width, button_height)
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], settings_rect)
        settings_text = SCORE_FONT.render("Settings", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(settings_text, (settings_rect.x + settings_rect.width // 2 - settings_text.get_width() // 2,
                                    settings_rect.y + settings_rect.height // 2 - settings_text.get_height() // 2))

        # "Main Menu" button
        main_menu_rect = pygame.Rect(button_x, 350, button_width, button_height)
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], main_menu_rect)
        main_menu_text = SCORE_FONT.render("Main Menu", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(main_menu_text, (main_menu_rect.x + main_menu_rect.width // 2 - main_menu_text.get_width() // 2,
                                     main_menu_rect.y + main_menu_rect.height // 2 - main_menu_text.get_height() // 2))

    def draw_select_mode(self):
        # Implement the select mode screen drawing
        pass  # Add your code here

    def draw_leaderboard(self):
        # Implement the leaderboard screen drawing
        WINDOW.fill(self.themes[self.theme]['background'])
        title = FONT.render("Leaderboard", True, self.themes[self.theme]['text'])
        WINDOW.blit(title, (WINDOW_SIZE // 2 - title.get_width() // 2, 50))
        y_offset = 100
        sorted_leaderboard = sorted(self.leaderboard.items(), key=lambda x: x[1], reverse=True)
        for name, score in sorted_leaderboard:
            entry_text = SCORE_FONT.render(f"{name}: {score}", True, self.themes[self.theme]['text'])
            WINDOW.blit(entry_text, (WINDOW_SIZE // 2 - entry_text.get_width() // 2, y_offset))
            y_offset += 30

        # Draw Back Button
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], self.back_button_rect)
        back_text = SCORE_FONT.render("Back", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5))

    def draw_pause_menu(self):
        # Implement the pause menu drawing
        pass  # Add your code here

    def set_game_mode(self, mode):
        self.game_mode = mode
        print(f"Game mode set to {self.game_mode}")

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        print(f"Difficulty set to {self.difficulty}")

    def set_ai_personality(self, personality):
        self.ai_personality = personality
        print(f"AI Personality set to {self.ai_personality}")

    def toggle_theme(self):
        self.theme = 'Dark' if self.theme == 'Light' else 'Light'
        self.update_theme()
        print(f"Theme toggled to {self.theme}")

    def update_theme(self):
        self.input_box.update_theme(self.themes[self.theme])
        # Update other UI elements if necessary

    def save_scores(self):
        try:
            with open(self.save_file, 'w') as f:
                json.dump({
                    'player_score': self.player_score,
                    'ai_score': self.ai_score,
                    'player_wins': self.player_wins,
                    'ai_wins': self.ai_wins,
                    'ties': self.ties,
                    'total_games': self.total_games,
                    'player_name': self.player_name,
                    'ai_name': self.ai_name,
                }, f)
        except IOError as e:
            print(f"Error saving scores: {e}")

    def load_scores(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.player_score = data.get('player_score', 0)
                    self.ai_score = data.get('ai_score', 0)
                    self.player_wins = data.get('player_wins', 0)
                    self.ai_wins = data.get('ai_wins', 0)
                    self.ties = data.get('ties', 0)
                    self.total_games = data.get('total_games', 0)
                    self.player_name = data.get('player_name', 'Player')
                    self.ai_name = data.get('ai_name', 'AI')
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading scores: {e}")
                print("Failed to load scores. Starting fresh.")
                self.reset_scores()
        else:
            self.reset_scores()

    def reset_scores(self):
        self.player_score = 0
        self.ai_score = 0
        self.player_wins = 0
        self.ai_wins = 0
        self.ties = 0
        self.total_games = 0

    def update_leaderboard(self):
        # Update the leaderboard with the player's score
        self.leaderboard[self.player_name] = self.player_score
        self.save_leaderboard()

    def save_leaderboard(self):
        try:
            with open(self.leaderboard_file, 'w') as f:
                json.dump(self.leaderboard, f)
        except IOError as e:
            print(f"Error saving leaderboard: {e}")

    def load_leaderboard(self):
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r') as f:
                    self.leaderboard = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading leaderboard: {e}")
                print("Failed to load leaderboard. Starting fresh.")
                self.leaderboard = {}
        else:
            self.leaderboard = {}

    def save_theme(self):
        try:
            with open(self.theme_file, 'w') as f:
                json.dump({'theme': self.theme}, f)
        except IOError as e:
            print(f"Error saving theme: {e}")

    def load_theme(self):
        if os.path.exists(self.theme_file):
            try:
                with open(self.theme_file, 'r') as f:
                    data = json.load(f)
                    self.theme = data.get('theme', 'Light')
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading theme: {e}")
                print("Failed to load theme. Using default theme.")
                self.theme = 'Light'
        else:
            self.theme = 'Light'

if __name__ == "__main__":
    # Create the game instance
    game = TicTacToe()