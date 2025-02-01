import pygame
import sys
import random
import time
import os
import json
import math

"""
Enhanced Tic-Tac-Toe with:
 - Undo/Redo support
 - Improved AI (memoization, variable depth, and a simple learning AI)
 - Additional board sizes (3x3, 4x4, 5x5)
 - Hint system
 - In-game Help Screen
 - Enhanced Animations (fade transitions, animated move placements, and particle effects)
 - Basic Sound & Music integration (the “old” sound method)
 - **Data & Persistence Enhancements:**
      • Robust save/load supporting multiple user profiles and game history.
      • Enhanced leaderboard entries including date and game mode.
      
Author: Jeremiah Ddumba
"""

pygame.init()
pygame.mixer.init()

# Set up the game window
WINDOW_SIZE = 600
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
    'hint': (255, 0, 0)
}

DARK_THEME = {
    'background': (34, 34, 34),
    'grid': (255, 255, 255),
    'text': (255, 255, 255),
    'highlight': (70, 130, 180),
    'button': (105, 105, 105),
    'button_text': (255, 255, 255),
    'input_box_active': (255, 215, 0),
    'hint': (255, 69, 0)
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
GAME_OVER = 'game_over'
LEADERBOARD = 'leaderboard'
HELP = 'help'
SELECT_MODE = 'select_mode'

# --- Helper Functions for Animations ---
def fade(screen, color, duration=500):
    """Fade to a solid color over duration (ms)"""
    fade_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
    fade_surface.fill(color)
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0,0))
        pygame.display.update()
        pygame.time.delay(duration // 50)

def play_particle_effect(start_pos, end_pos, theme_color):
    """Simple particle effect along a line between start_pos and end_pos."""
    particles = []
    for i in range(20):
        t = i / 20.0
        x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
        y = start_pos[1] + (end_pos[1] - start_pos[1]) * t
        particles.append([x, y, random.uniform(-1, 1), random.uniform(-1, 1), random.randint(4,8)])
    for _ in range(20):
        for p in particles:
            p[0] += p[2]
            p[1] += p[3]
            p[4] = max(0, p[4]-0.5)
        WINDOW.fill((0,0,0,0))
        for p in particles:
            if p[4] > 0:
                pygame.draw.circle(WINDOW, theme_color, (int(p[0]), int(p[1])), int(p[4]))
        pygame.display.update()
        pygame.time.delay(30)

# --- Classes ---
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (0, 0, 0)
        self.color_active = (255, 255, 0)
        self.color = self.color_inactive
        self.text = text
        self.active = False
        self.txt_surface = FONT.render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
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
        surface.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(surface, self.color, self.rect, 2)

    def update_theme(self, theme):
        self.color_inactive = theme['text']
        self.color_active = theme['input_box_active']
        self.color = self.color_active if self.active else self.color_inactive
        self.txt_surface = FONT.render(self.text, True, self.color)

class TicTacToe:
    def __init__(self):
        # Game configuration
        self.board_size = 3  # 3x3 board
        self.win_length = self.board_size
        self.misere_mode = False
        self.board = [''] * (self.board_size * self.board_size)
        self.current_player = 'X'
        self.player_score = 0
        self.ai_score = 0
        self.player_wins = 0
        self.ai_wins = 0
        self.ties = 0
        self.total_games = 0

        # AI configuration
        self.difficulty = 'Easy'
        self.ai_depth = 9
        self.ai_personality = 'Balanced'
        self.learning_table = {}

        # Game mode
        self.game_mode = 'Player vs AI'
        
        # Set default AI name
        self.ai_name = "AI"

        # Animation timing
        self.animation_speed = 100

        # UI and drawing
        self.running = True
        self.cell_size = WINDOW_SIZE // self.board_size
        self.update_grid_lines()

        # Undo/Redo tracking
        self.move_history = []
        self.redo_history = []

        self.last_move = None
        self.hint_index = None

        # Memoization for minimax
        self.memoization = {}

        # Game state
        self.state = MENU
        self.previous_state = None
        self.input_box = InputBox(200, 150, 200, 40)
        self.input_active = False
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.back_button_rect = pygame.Rect(10, 10, 80, 30)
        
        # Files for persistence, profiles, etc.
        self.save_file = 'scores.json'
        self.leaderboard_file = 'leaderboard.json'
        self.theme_file = 'theme.json'
        
        # New data attributes:
        self.profiles = {}      # holds profiles (multiple user data + game history)
        self.profile_name = "Player"  # default profile name
        
        # Leaderboard will now be a list of entries
        self.leaderboard = []

        self.themes = {'Light': LIGHT_THEME, 'Dark': DARK_THEME}

        # --- Old Sound Integration ---
        self.load_sounds()

        # For scrolling in settings
        self.settings_scroll_offset = 0
        self.content_height = 0
        self.settings_clickable_areas = []

        # Load saved configurations
        self.load_profiles()
        self.load_leaderboard()
        self.load_theme()
        self.update_theme()

        self.main_loop()

    # ===== Data Persistence Methods =====

    def load_profiles(self):
        """Load all user profiles (scores, stats, game history) from save_file."""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                    self.profiles = data.get("profiles", {})
            except (json.JSONDecodeError, IOError) as e:
                print("Error loading profiles:", e)
                self.profiles = {}
        else:
            self.profiles = {}
        # Ensure current profile exists:
        if self.profile_name not in self.profiles:
            self.profiles[self.profile_name] = {
                "player_score": 0,
                "ai_score": 0,
                "player_wins": 0,
                "ai_wins": 0,
                "ties": 0,
                "total_games": 0,
                "game_history": []
            }

    def save_profiles(self):
        """Save the profiles dictionary to the save_file."""
        try:
            with open(self.save_file, 'w') as f:
                json.dump({"profiles": self.profiles}, f)
        except IOError as e:
            print("Error saving profiles:", e)

    def update_current_profile(self, result):
        """
        Update the current profile with the latest game statistics and add a game history record.
        'result' is a string: "win", "loss", or "tie".
        """
        profile = self.profiles.get(self.profile_name, {
            "player_score": 0,
            "ai_score": 0,
            "player_wins": 0,
            "ai_wins": 0,
            "ties": 0,
            "total_games": 0,
            "game_history": []
        })
        profile["player_score"] = self.player_score
        profile["ai_score"] = self.ai_score
        profile["player_wins"] = self.player_wins
        profile["ai_wins"] = self.ai_wins
        profile["ties"] = self.ties
        profile["total_games"] = self.total_games
        game_record = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "result": result
            # You could add additional details (e.g., moves history) here if desired.
        }
        profile["game_history"].append(game_record)
        self.profiles[self.profile_name] = profile
        self.save_profiles()

    def load_leaderboard(self):
        """Load the enhanced leaderboard (a list of entries) from file."""
        if os.path.exists(self.leaderboard_file):
            try:
                with open(self.leaderboard_file, 'r') as f:
                    self.leaderboard = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print("Error loading leaderboard:", e)
                self.leaderboard = []
        else:
            self.leaderboard = []

    def save_leaderboard(self):
        """Save the leaderboard list to file."""
        try:
            with open(self.leaderboard_file, 'w') as f:
                json.dump(self.leaderboard, f)
        except IOError as e:
            print("Error saving leaderboard:", e)

    def update_leaderboard(self):
        """Append a new leaderboard entry with additional details and then sort."""
        entry = {
            "name": self.profile_name,
            "score": self.player_score,
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "mode": self.game_mode
        }
        self.leaderboard.append(entry)
        # Sort by score descending:
        self.leaderboard.sort(key=lambda x: x["score"], reverse=True)
        self.save_leaderboard()

    # ===== End Data Persistence Methods =====

    # ===== Sound, Theme, and Other Methods (unchanged from previous version) =====
    def load_sounds(self):
        try:
            # Using the “old” sound integration:
            self.move_sound = pygame.mixer.Sound("move.wav")
            self.win_sound = pygame.mixer.Sound("win.wav")
            self.tie_sound = pygame.mixer.Sound("tie.wav")
            self.button_click_sound = pygame.mixer.Sound("button_click.wav")
            pygame.mixer.music.load("bg_music.mp3")
            pygame.mixer.music.play(-1)
        except Exception as e:
            print("Error loading sound files:", e)
            self.move_sound = self.win_sound = self.tie_sound = self.button_click_sound = None

    def play_sound(self, sound):
        if sound is not None:
            sound.play()

    def update_grid_lines(self):
        self.cell_size = WINDOW_SIZE // self.board_size
        self.grid_lines = []
        for i in range(1, self.board_size):
            self.grid_lines.append(((i * self.cell_size, 0), (i * self.cell_size, WINDOW_SIZE)))
        for i in range(1, self.board_size):
            self.grid_lines.append(((0, i * self.cell_size), (WINDOW_SIZE, i * self.cell_size)))

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_profiles()
                self.save_leaderboard()
                self.save_theme()
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
                    elif event.key == pygame.K_u:
                        self.undo_move()
                    elif event.key == pygame.K_y:
                        self.redo_move()
                    elif event.key == pygame.K_i:
                        self.hint_index = self.get_hint_move()
            elif self.state == PAUSE:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = GAME
                    elif event.key == pygame.K_ESCAPE:
                        self.state = MENU
            elif self.state == SETTINGS:
                result = self.input_box.handle_event(event)
                if result is not None:
                    if result != '':
                        self.profile_name = result  # update the profile name
                        self.show_message(f"Profile set to {self.profile_name}")
                        if self.previous_state == GAME_OVER:
                            self.reset_board()
                            self.state = GAME
                        else:
                            self.state = MENU
                    else:
                        self.show_message("Name cannot be empty!")
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.settings_scroll_offset += 20
                        if self.settings_scroll_offset > 0:
                            self.settings_scroll_offset = 0
                    elif event.button == 5:
                        max_scroll = min(0, WINDOW_SIZE - self.content_height)
                        self.settings_scroll_offset -= 20
                        if self.settings_scroll_offset < max_scroll:
                            self.settings_scroll_offset = max_scroll
                    else:
                        adjusted_pos = (event.pos[0], event.pos[1] - self.settings_scroll_offset)
                        self.handle_settings_click(adjusted_pos)
            elif self.state == GAME_OVER:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_game_over_click(event.pos)
            elif self.state == HELP:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.state = MENU
            elif self.state == SELECT_MODE:
                if event.type == pygame.KEYDOWN:
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
        WINDOW_SIZE = min(width, height)
        if WINDOW_SIZE < 300:
            WINDOW_SIZE = 300
        WINDOW = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE), pygame.RESIZABLE)
        self.update_grid_lines()

    def handle_back_button(self, pos):
        if self.back_button_rect.collidepoint(pos):
            self.state = MENU
            self.play_sound(self.button_click_sound)

    def handle_menu_click(self, pos):
        x, y = pos
        button_width = WINDOW_SIZE * 0.4
        button_height = WINDOW_SIZE * 0.08
        button_x = WINDOW_SIZE // 2 - button_width // 2

        # Play button
        if button_x <= x <= button_x + button_width and WINDOW_SIZE * 0.25 <= y <= WINDOW_SIZE * 0.25 + button_height:
            self.play_sound(self.button_click_sound)
            self.state = GAME
            self.reset_board()
        # Settings button
        elif button_x <= x <= button_x + button_width and WINDOW_SIZE * 0.35 <= y <= WINDOW_SIZE * 0.35 + button_height:
            self.play_sound(self.button_click_sound)
            self.previous_state = MENU
            self.state = SETTINGS
        # Help button
        elif button_x <= x <= button_x + button_width and WINDOW_SIZE * 0.45 <= y <= WINDOW_SIZE * 0.45 + button_height:
            self.play_sound(self.button_click_sound)
            self.state = HELP
        # Leaderboard button
        elif button_x <= x <= button_x + button_width and WINDOW_SIZE * 0.55 <= y <= WINDOW_SIZE * 0.55 + button_height:
            self.play_sound(self.button_click_sound)
            self.state = LEADERBOARD
        # Exit button
        elif button_x <= x <= button_x + button_width and WINDOW_SIZE * 0.65 <= y <= WINDOW_SIZE * 0.65 + button_height:
            self.save_profiles()
            self.save_leaderboard()
            self.save_theme()
            pygame.quit()
            sys.exit()

    def handle_settings_click(self, pos):
        self.handle_back_button(pos)
        pos = (pos[0], pos[1] + self.settings_scroll_offset)
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
                elif action == 'set_board_size':
                    self.set_board_size(value)
                elif action == 'toggle_misere':
                    self.misere_mode = not self.misere_mode
                    self.show_message(f"Misère Mode {'On' if self.misere_mode else 'Off'}")
                if self.previous_state == GAME_OVER:
                    self.reset_board()
                    self.state = GAME
                break

    def handle_select_mode_click(self, pos):
        x, y = pos
        if 200 <= x <= 400:
            if 190 <= y <= 220:
                self.set_game_mode('Player vs AI')
            elif 230 <= y <= 260:
                self.set_game_mode('Player vs Player')
            elif 270 <= y <= 300:
                self.set_game_mode('AI vs AI')
            elif 370 <= y <= 400:
                self.set_difficulty('Easy')
            elif 410 <= y <= 440:
                self.set_difficulty('Medium')
            elif 450 <= y <= 480:
                self.set_difficulty('Hard')
        self.state = MENU

    def handle_game_over_click(self, pos):
        if 200 <= pos[0] <= 400:
            if 250 <= pos[1] <= 290:
                self.reset_board()
                self.state = GAME
            elif 300 <= pos[1] <= 340:
                self.previous_state = GAME_OVER
                self.state = SETTINGS
            elif 350 <= pos[1] <= 390:
                self.state = MENU

    def handle_leaderboard_click(self, pos):
        self.handle_back_button(pos)

    def handle_click(self, pos):
        x, y = pos
        row = y // self.cell_size
        col = x // self.cell_size
        index = row * self.board_size + col
        if 0 <= index < len(self.board) and self.board[index] == '':
            self.make_move(index)
            self.play_sound(self.move_sound)
        self.handle_back_button(pos)
        self.hint_index = None

    def make_move(self, index):
        if self.board[index] == '':
            self.move_history.append((self.board.copy(), self.current_player))
            self.redo_history.clear()
            self.board[index] = self.current_player
            self.last_move = index
            self.animate_move(index)
            if self.check_winner(self.board, self.current_player):
                # Update current profile stats before leaderboard update.
                self.total_games += 1
                if self.current_player == 'X':
                    self.player_wins += 1
                else:
                    self.ai_wins += 1
                self.update_current_profile("win" if self.current_player=='X' else "loss")
                self.handle_win(self.current_player)
            elif '' not in self.board:
                self.total_games += 1
                self.ties += 1
                self.update_current_profile("tie")
                self.handle_tie()
            else:
                self.switch_turns()
                if self.game_mode == 'Player vs AI' and self.current_player == 'O':
                    self.ai_move()
                elif self.game_mode == 'AI vs AI':
                    self.ai_move()

    def animate_move(self, index):
        x = (index % self.board_size) * self.cell_size
        y = (index // self.board_size) * self.cell_size
        for scale in range(5, 15, 2):
            temp_surface = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            if self.current_player == 'X':
                padding = self.cell_size // 4
                start_pos = (padding, padding)
                end_pos = (self.cell_size - padding, self.cell_size - padding)
                pygame.draw.line(temp_surface, self.themes[self.theme]['text'], start_pos, end_pos, 5)
                start_pos = (self.cell_size - padding, padding)
                end_pos = (padding, self.cell_size - padding)
                pygame.draw.line(temp_surface, self.themes[self.theme]['text'], start_pos, end_pos, 5)
            elif self.current_player == 'O':
                center = (self.cell_size//2, self.cell_size//2)
                radius = self.cell_size//2 - self.cell_size//4
                pygame.draw.circle(temp_surface, self.themes[self.theme]['text'], center, radius, 5)
            temp_surface = pygame.transform.scale(temp_surface, (scale, scale))
            WINDOW.fill(self.themes[self.theme]['background'])
            self.draw_game()
            WINDOW.blit(temp_surface, (x + self.cell_size//2 - scale//2, y + self.cell_size//2 - scale//2))
            pygame.display.update()
            pygame.time.delay(20)

    def undo_move(self):
        if self.move_history:
            self.redo_history.append((self.board.copy(), self.current_player))
            state = self.move_history.pop()
            self.board, self.current_player = state
            self.last_move = None
            self.show_message("Undo performed")
        else:
            self.show_message("Nothing to undo!")

    def redo_move(self):
        if self.redo_history:
            self.move_history.append((self.board.copy(), self.current_player))
            state = self.redo_history.pop()
            self.board, self.current_player = state
            self.last_move = None
            self.show_message("Redo performed")
        else:
            self.show_message("Nothing to redo!")

    def switch_player(self, player):
        return 'O' if player == 'X' else 'X'

    def switch_turns(self):
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
            elif self.ai_personality == 'Learning':
                index = self.learning_move(empty_indices)
            else:
                index = self.minimax_ai()
        self.make_move(index)
        if self.game_mode == 'AI vs AI':
            pygame.time.wait(500)

    def aggressive_move(self, empty_indices):
        for index in empty_indices:
            self.board[index] = self.current_player
            if self.check_winner(self.board, self.current_player):
                self.board[index] = ''
                return index
            self.board[index] = ''
        return random.choice(empty_indices)

    def defensive_move(self, empty_indices):
        opponent = self.switch_player(self.current_player)
        for index in empty_indices:
            self.board[index] = opponent
            if self.check_winner(self.board, opponent):
                self.board[index] = ''
                return index
            self.board[index] = ''
        return random.choice(empty_indices)

    def block_player(self, empty_indices):
        for index in empty_indices:
            self.board[index] = self.current_player
            if self.check_winner(self.board, self.current_player):
                self.board[index] = ''
                return index
            self.board[index] = ''
        opponent = self.switch_player(self.current_player)
        for index in empty_indices:
            self.board[index] = opponent
            if self.check_winner(self.board, opponent):
                self.board[index] = ''
                return index
            self.board[index] = ''
        if 4 in empty_indices:
            return 4
        return random.choice(empty_indices)

    def minimax_ai(self):
        best_score = -float('inf')
        best_move = None
        for i in range(len(self.board)):
            if self.board[i] == '':
                self.board[i] = self.current_player
                score = self.minimax(self.board, self.switch_player(self.current_player), False, self.ai_depth)
                self.board[i] = ''
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, player, is_maximizing, depth, alpha=-float('inf'), beta=float('inf')):
        board_key = tuple(board)
        if (board_key, player, is_maximizing, depth) in self.memoization:
            return self.memoization[(board_key, player, is_maximizing, depth)]

        opponent = self.switch_player(player)
        if self.check_winner(board, opponent):
            score = 1 if opponent == self.current_player else -1
            self.memoization[(board_key, player, is_maximizing, depth)] = score
            return score
        elif '' not in board or depth == 0:
            return 0

        if is_maximizing:
            max_eval = -float('inf')
            for i in range(len(board)):
                if board[i] == '':
                    board[i] = player
                    eval = self.minimax(board, self.switch_player(player), False, depth - 1, alpha, beta)
                    board[i] = ''
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            self.memoization[(board_key, player, is_maximizing, depth)] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(len(board)):
                if board[i] == '':
                    board[i] = player
                    eval = self.minimax(board, self.switch_player(player), True, depth - 1, alpha, beta)
                    board[i] = ''
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            self.memoization[(board_key, player, is_maximizing, depth)] = min_eval
            return min_eval

    def learning_move(self, empty_indices):
        board_key = tuple(self.board)
        if board_key in self.learning_table:
            moves = self.learning_table[board_key]
            available_moves = {move: wins for move, wins in moves.items() if move in empty_indices}
            if available_moves:
                return max(available_moves, key=available_moves.get)
        return self.minimax_ai()

    def check_winner(self, board, player):
        n = self.board_size
        win = False
        for i in range(n):
            if all(board[i*n + j] == player for j in range(n)):
                win = True
            if all(board[j*n + i] == player for j in range(n)):
                win = True
        if all(board[i*n + i] == player for i in range(n)):
            win = True
        if all(board[i*n + (n - 1 - i)] == player for i in range(n)):
            win = True
        if self.misere_mode:
            return not win and any(board[i] != '' for i in range(len(board)))
        else:
            return win

    def draw_winning_line(self, combo):
        start_index = combo[0]
        end_index = combo[-1]
        start_pos = ((start_index % self.board_size) * self.cell_size + self.cell_size // 2,
                     (start_index // self.board_size) * self.cell_size + self.cell_size // 2)
        end_pos = ((end_index % self.board_size) * self.cell_size + self.cell_size // 2,
                   (end_index // self.board_size) * self.cell_size + self.cell_size // 2)
        for thickness in range(1, 8):
            pygame.draw.line(WINDOW, self.themes[self.theme]['highlight'], start_pos, end_pos, thickness)
            pygame.display.update()
            pygame.time.delay(50)
        play_particle_effect(start_pos, end_pos, self.themes[self.theme]['highlight'])

    def handle_win(self, winner):
        self.total_games += 1
        if winner == 'X':
            self.player_score += 1
            self.player_wins += 1
            message = f"{self.profile_name} wins!"
            self.update_leaderboard()
            self.update_current_profile("win")
        else:
            self.ai_score += 1
            self.ai_wins += 1
            message = f"{self.ai_name} wins!"
            if self.ai_personality == 'Learning':
                board_key = tuple(self.board)
                if board_key not in self.learning_table:
                    self.learning_table[board_key] = {}
                move = self.last_move
                self.learning_table[board_key][move] = self.learning_table[board_key].get(move, 0) + 1
            self.update_current_profile("loss")
        self.play_sound(self.win_sound)
        self.fade_game_over(message)
        self.state = GAME_OVER

    def handle_tie(self):
        self.ties += 1
        self.total_games += 1
        self.update_current_profile("tie")
        self.play_sound(self.tie_sound)
        self.fade_game_over("It's a tie!")
        self.state = GAME_OVER

    def fade_game_over(self, message):
        text_surface = FONT.render(message, True, self.themes[self.theme]['text'])
        rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        for alpha in range(0, 255, 10):
            fade_surface = pygame.Surface((WINDOW_SIZE, WINDOW_SIZE))
            fade_surface.fill(self.themes[self.theme]['background'])
            fade_surface.set_alpha(alpha)
            WINDOW.blit(text_surface, rect)
            WINDOW.blit(fade_surface, (0, 0))
            pygame.display.update()
            pygame.time.delay(30)
        pygame.time.delay(1000)

    def show_message(self, message):
        text_surface = FONT.render(message, True, self.themes[self.theme]['text'])
        rect = text_surface.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2))
        WINDOW.blit(text_surface, rect)
        pygame.display.update()
        pygame.time.delay(1500)

    def reset_board(self):
        self.board = [''] * (self.board_size * self.board_size)
        self.current_player = 'X'
        self.last_move = None
        self.move_history.clear()
        self.redo_history.clear()
        self.memoization.clear()
        self.hint_index = None
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
        elif self.state == HELP:
            self.draw_help()
        elif self.state == SELECT_MODE:
            self.draw_select_mode()
        elif self.state == LEADERBOARD:
            self.draw_leaderboard()

    def draw_menu(self):
        WINDOW.fill(self.themes[self.theme]['background'])
        title = FONT.render("Tic-Tac-Toe", True, self.themes[self.theme]['text'])
        WINDOW.blit(title, (WINDOW_SIZE // 2 - title.get_width() // 2, WINDOW_SIZE * 0.1))
        button_width = WINDOW_SIZE * 0.4
        button_height = WINDOW_SIZE * 0.08
        button_x = WINDOW_SIZE // 2 - button_width // 2

        mouse_pos = pygame.mouse.get_pos()
        def draw_button(y, text):
            rect = pygame.Rect(button_x, y, button_width, button_height)
            color = self.themes[self.theme]['button']
            if rect.collidepoint(mouse_pos):
                color = tuple(min(255, c + 30) for c in color)
            pygame.draw.rect(WINDOW, color, rect)
            txt = FONT.render(text, True, self.themes[self.theme]['button_text'])
            WINDOW.blit(txt, (rect.x + rect.width // 2 - txt.get_width() // 2,
                              rect.y + rect.height // 2 - txt.get_height() // 2))
        draw_button(WINDOW_SIZE * 0.25, "Play")
        draw_button(WINDOW_SIZE * 0.35, "Settings")
        draw_button(WINDOW_SIZE * 0.45, "Help")
        draw_button(WINDOW_SIZE * 0.55, "Leaderboard")
        draw_button(WINDOW_SIZE * 0.65, "Exit")

    def draw_game(self):
        WINDOW.fill(self.themes[self.theme]['background'])
        for line in self.grid_lines:
            pygame.draw.line(WINDOW, self.themes[self.theme]['grid'], line[0], line[1], 2)
        if self.last_move is not None:
            x = (self.last_move % self.board_size) * self.cell_size
            y = (self.last_move // self.board_size) * self.cell_size
            highlight_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(WINDOW, self.themes[self.theme]['highlight'], highlight_rect)
        for i in range(len(self.board)):
            x = (i % self.board_size) * self.cell_size
            y = (i // self.board_size) * self.cell_size
            if self.board[i] == 'X':
                self.draw_x(x, y)
            elif self.board[i] == 'O':
                self.draw_o(x, y)
        if self.hint_index is not None:
            x = (self.hint_index % self.board_size) * self.cell_size
            y = (self.hint_index // self.board_size) * self.cell_size
            hint_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
            pygame.draw.rect(WINDOW, self.themes[self.theme]['hint'], hint_rect, 4)
        self.draw_scores()
        self.draw_stats()
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], self.back_button_rect)
        back_text = SCORE_FONT.render("Back", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5))

    def draw_x(self, x, y):
        padding = self.cell_size // 4
        start_pos = (x + padding, y + padding)
        end_pos = (x + self.cell_size - padding, y + self.cell_size - padding)
        pygame.draw.line(WINDOW, self.themes[self.theme]['text'], start_pos, end_pos, 5)
        start_pos = (x + self.cell_size - padding, y + padding)
        end_pos = (x + padding, y + self.cell_size - padding)
        pygame.draw.line(WINDOW, self.themes[self.theme]['text'], start_pos, end_pos, 5)

    def draw_o(self, x, y):
        center = (x + self.cell_size // 2, y + self.cell_size // 2)
        radius = self.cell_size // 2 - self.cell_size // 4
        pygame.draw.circle(WINDOW, self.themes[self.theme]['text'], center, radius, 5)

    def draw_scores(self):
        score_text = SCORE_FONT.render(f"{self.profile_name}: {self.player_score}    {self.ai_name}: {self.ai_score}", True, self.themes[self.theme]['text'])
        WINDOW.blit(score_text, (WINDOW_SIZE // 2 - score_text.get_width() // 2, 10))

    def draw_stats(self):
        stats_text = STATS_FONT.render(f"Total Games: {self.total_games}    Wins: {self.player_wins}    Losses: {self.ai_wins}    Ties: {self.ties}", True, self.themes[self.theme]['text'])
        WINDOW.blit(stats_text, (WINDOW_SIZE // 2 - stats_text.get_width() // 2, 30))

    def draw_settings(self):
        WINDOW.fill(self.themes[self.theme]['background'])
        y_offset = 50 + self.settings_scroll_offset
        self.settings_clickable_areas = []
        title = FONT.render("Settings", True, self.themes[self.theme]['text'])
        WINDOW.blit(title, (WINDOW_SIZE//2 - title.get_width()//2, y_offset))
        y_offset += 60

        name_label = FONT.render("Enter profile name:", True, self.themes[self.theme]['text'])
        WINDOW.blit(name_label, (WINDOW_SIZE//2 - name_label.get_width()//2, y_offset))
        y_offset += 40

        self.input_box.rect.y = y_offset
        self.input_box.draw(WINDOW)
        y_offset += self.input_box.rect.height + 20

        difficulty_label = FONT.render("Select Difficulty:", True, self.themes[self.theme]['text'])
        WINDOW.blit(difficulty_label, (WINDOW_SIZE//2 - difficulty_label.get_width()//2, y_offset))
        y_offset += 30

        easy_button = SCORE_FONT.render("Easy", True, self.themes[self.theme]['text'])
        easy_button_rect = easy_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_difficulty', 'Easy', easy_button_rect))
        WINDOW.blit(easy_button, easy_button_rect)
        y_offset += 40

        medium_button = SCORE_FONT.render("Medium", True, self.themes[self.theme]['text'])
        medium_button_rect = medium_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_difficulty', 'Medium', medium_button_rect))
        WINDOW.blit(medium_button, medium_button_rect)
        y_offset += 40

        hard_button = SCORE_FONT.render("Hard", True, self.themes[self.theme]['text'])
        hard_button_rect = hard_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_difficulty', 'Hard', hard_button_rect))
        WINDOW.blit(hard_button, hard_button_rect)
        y_offset += 60

        mode_label = FONT.render("Select Game Mode:", True, self.themes[self.theme]['text'])
        WINDOW.blit(mode_label, (WINDOW_SIZE//2 - mode_label.get_width()//2, y_offset))
        y_offset += 30

        p_vs_ai_button = SCORE_FONT.render("Player vs AI", True, self.themes[self.theme]['text'])
        p_vs_ai_button_rect = p_vs_ai_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_game_mode', 'Player vs AI', p_vs_ai_button_rect))
        WINDOW.blit(p_vs_ai_button, p_vs_ai_button_rect)
        y_offset += 40

        p_vs_p_button = SCORE_FONT.render("Player vs Player", True, self.themes[self.theme]['text'])
        p_vs_p_button_rect = p_vs_p_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_game_mode', 'Player vs Player', p_vs_p_button_rect))
        WINDOW.blit(p_vs_p_button, p_vs_p_button_rect)
        y_offset += 40

        ai_vs_ai_button = SCORE_FONT.render("AI vs AI", True, self.themes[self.theme]['text'])
        ai_vs_ai_button_rect = ai_vs_ai_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_game_mode', 'AI vs AI', ai_vs_ai_button_rect))
        WINDOW.blit(ai_vs_ai_button, ai_vs_ai_button_rect)
        y_offset += 60

        theme_button = SCORE_FONT.render(f"Toggle Theme (Current: {self.theme})", True, self.themes[self.theme]['text'])
        theme_button_rect = theme_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('toggle_theme', None, theme_button_rect))
        WINDOW.blit(theme_button, theme_button_rect)
        y_offset += 40

        personality_label = FONT.render("Select AI Personality:", True, self.themes[self.theme]['text'])
        WINDOW.blit(personality_label, (WINDOW_SIZE//2 - personality_label.get_width()//2, y_offset))
        y_offset += 30

        aggressive_button = SCORE_FONT.render("Aggressive", True, self.themes[self.theme]['text'])
        aggressive_button_rect = aggressive_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_ai_personality', 'Aggressive', aggressive_button_rect))
        WINDOW.blit(aggressive_button, aggressive_button_rect)
        y_offset += 40

        defensive_button = SCORE_FONT.render("Defensive", True, self.themes[self.theme]['text'])
        defensive_button_rect = defensive_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_ai_personality', 'Defensive', defensive_button_rect))
        WINDOW.blit(defensive_button, defensive_button_rect)
        y_offset += 40

        balanced_button = SCORE_FONT.render("Balanced", True, self.themes[self.theme]['text'])
        balanced_button_rect = balanced_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_ai_personality', 'Balanced', balanced_button_rect))
        WINDOW.blit(balanced_button, balanced_button_rect)
        y_offset += 40

        learning_button = SCORE_FONT.render("Learning", True, self.themes[self.theme]['text'])
        learning_button_rect = learning_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_ai_personality', 'Learning', learning_button_rect))
        WINDOW.blit(learning_button, learning_button_rect)
        y_offset += 60

        board_size_label = FONT.render("Select Board Size:", True, self.themes[self.theme]['text'])
        WINDOW.blit(board_size_label, (WINDOW_SIZE//2 - board_size_label.get_width()//2, y_offset))
        y_offset += 30

        size_3_button = SCORE_FONT.render("3 x 3", True, self.themes[self.theme]['text'])
        size_3_button_rect = size_3_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_board_size', 3, size_3_button_rect))
        WINDOW.blit(size_3_button, size_3_button_rect)
        y_offset += 40

        size_4_button = SCORE_FONT.render("4 x 4", True, self.themes[self.theme]['text'])
        size_4_button_rect = size_4_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_board_size', 4, size_4_button_rect))
        WINDOW.blit(size_4_button, size_4_button_rect)
        y_offset += 40

        size_5_button = SCORE_FONT.render("5 x 5", True, self.themes[self.theme]['text'])
        size_5_button_rect = size_5_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('set_board_size', 5, size_5_button_rect))
        WINDOW.blit(size_5_button, size_5_button_rect)
        y_offset += 60

        misere_button = SCORE_FONT.render(f"Toggle Misère Mode (Current: {'On' if self.misere_mode else 'Off'})", True, self.themes[self.theme]['text'])
        misere_button_rect = misere_button.get_rect(topleft=(200, y_offset))
        self.settings_clickable_areas.append(('toggle_misere', None, misere_button_rect))
        WINDOW.blit(misere_button, misere_button_rect)
        y_offset += 40

        self.content_height = y_offset - self.settings_scroll_offset
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], self.back_button_rect)
        back_text = SCORE_FONT.render("Back", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5))

    def draw_help(self):
        WINDOW.fill(self.themes[self.theme]['background'])
        title = FONT.render("Help & Instructions", True, self.themes[self.theme]['text'])
        WINDOW.blit(title, (WINDOW_SIZE // 2 - title.get_width() // 2, 30))
        instructions = [
            "Gameplay Features:",
            "- Undo: Press U to undo the last move",
            "- Redo: Press Y to redo an undone move",
            "- Hint: Press I to show a recommended move",
            "- Pause: Press P to pause the game",
            "",
            "AI & Difficulty:",
            "- Press E, M, or H to set AI difficulty",
            "- Adjust AI personality and board size in Settings",
            "",
            "Sound:",
            "- Sounds play on moves, wins/ties, and button clicks",
            "",
            "Data Persistence:",
            "- Your profile (name, stats, and game history) is saved automatically.",
            "",
            "Leaderboard:",
            "- Leaderboard entries include your score, date, and game mode.",
            "",
            "Navigation:",
            "- Click Back to return to the Main Menu",
            "",
            "Click anywhere to return to the Main Menu"
        ]
        y_offset = 80
        for line in instructions:
            line_surface = STATS_FONT.render(line, True, self.themes[self.theme]['text'])
            WINDOW.blit(line_surface, (40, y_offset))
            y_offset += 25

    def draw_game_over(self):
        WINDOW.fill(self.themes[self.theme]['background'])
        message = FONT.render("Game Over!", True, self.themes[self.theme]['text'])
        WINDOW.blit(message, (WINDOW_SIZE // 2 - message.get_width() // 2, WINDOW_SIZE * 0.2))
        button_width = 200
        button_height = 40
        button_x = WINDOW_SIZE // 2 - button_width // 2

        play_again_rect = pygame.Rect(button_x, 250, button_width, button_height)
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], play_again_rect)
        play_again_text = SCORE_FONT.render("Play Again", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(play_again_text, (play_again_rect.x + play_again_rect.width // 2 - play_again_text.get_width() // 2,
                                      play_again_rect.y + play_again_rect.height // 2 - play_again_text.get_height() // 2))

        settings_rect = pygame.Rect(button_x, 300, button_width, button_height)
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], settings_rect)
        settings_text = SCORE_FONT.render("Settings", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(settings_text, (settings_rect.x + settings_rect.width // 2 - settings_text.get_width() // 2,
                                    settings_rect.y + settings_rect.height // 2 - settings_text.get_height() // 2))

        main_menu_rect = pygame.Rect(button_x, 350, button_width, button_height)
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], main_menu_rect)
        main_menu_text = SCORE_FONT.render("Main Menu", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(main_menu_text, (main_menu_rect.x + main_menu_rect.width // 2 - main_menu_text.get_width() // 2,
                                     main_menu_rect.y + main_menu_rect.height // 2 - main_menu_text.get_height() // 2))

    def draw_select_mode(self):
        pass

    def draw_leaderboard(self):
        WINDOW.fill(self.themes[self.theme]['background'])
        title = FONT.render("Leaderboard", True, self.themes[self.theme]['text'])
        WINDOW.blit(title, (WINDOW_SIZE // 2 - title.get_width() // 2, 50))
        y_offset = 100
        # Display each leaderboard entry with additional details.
        for entry in self.leaderboard:
            entry_text = SCORE_FONT.render(f"{entry['name']} | {entry['score']} | {entry['date']} | {entry['mode']}", True, self.themes[self.theme]['text'])
            WINDOW.blit(entry_text, (WINDOW_SIZE // 2 - entry_text.get_width() // 2, y_offset))
            y_offset += 30
        pygame.draw.rect(WINDOW, self.themes[self.theme]['button'], self.back_button_rect)
        back_text = SCORE_FONT.render("Back", True, self.themes[self.theme]['button_text'])
        WINDOW.blit(back_text, (self.back_button_rect.x + 10, self.back_button_rect.y + 5))

    def draw_pause_menu(self):
        pause_text = FONT.render("Paused. Press P to resume.", True, self.themes[self.theme]['text'])
        WINDOW.blit(pause_text, (WINDOW_SIZE//2 - pause_text.get_width()//2, WINDOW_SIZE//2 - pause_text.get_height()//2))

    def set_game_mode(self, mode):
        self.game_mode = mode
        print(f"Game mode set to {self.game_mode}")

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        print(f"Difficulty set to {self.difficulty}")

    def set_ai_personality(self, personality):
        self.ai_personality = personality
        print(f"AI Personality set to {self.ai_personality}")

    def set_board_size(self, size):
        self.board_size = size
        self.win_length = size
        self.reset_board()
        self.update_grid_lines()
        print(f"Board size set to {size}x{size}")

    def toggle_theme(self):
        self.theme = 'Dark' if self.theme == 'Light' else 'Light'
        self.update_theme()
        print(f"Theme toggled to {self.theme}")

    def update_theme(self):
        self.input_box.update_theme(self.themes[self.theme])

    def get_hint_move(self):
        empty_indices = [i for i, x in enumerate(self.board) if x == '']
        if not empty_indices:
            return None
        return self.minimax_ai()

    # ===== Original save_scores and load_scores have been replaced by the profiles methods =====

    def load_theme(self):
        if os.path.exists(self.theme_file):
            try:
                with open(self.theme_file, 'r') as f:
                    data = json.load(f)
                    self.theme = data.get('theme', 'Light')
            except (json.JSONDecodeError, IOError) as e:
                print("Error loading theme:", e)
                self.theme = 'Light'
        else:
            self.theme = 'Light'

    def save_theme(self):
        try:
            with open(self.theme_file, 'w') as f:
                json.dump({'theme': self.theme}, f)
        except IOError as e:
            print("Error saving theme:", e)

if __name__ == "__main__":
    game = TicTacToe()