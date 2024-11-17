import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from functools import partial
import pygame
import sys
import time

# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Load sound effects
MOVE_SOUND = pygame.mixer.Sound('move.wav')       # Sound for a move
WIN_SOUND = pygame.mixer.Sound('win.wav')         # Sound for a win
TIE_SOUND = pygame.mixer.Sound('tie.wav')         # Sound for a tie

"""
Program Name: Tic-Tac-Toe with AI and Enhanced Features
Author: [Jeremiah Ddumba]
Email: [jsd5521@psu.edu]
Extra Credit 
Assignment: Final Project - Tic-Tac-Toe with Difficulty Levels and Enhancements
Due Date: [Insert Date]
File Name: tic_tac_toe_gui.py
Program Purpose: Play Tic-Tac-Toe with various game modes, AI difficulty levels, track detailed statistics, and enhanced user experience with sounds and animations.
Compiler: Python 3.12
Operating System: [MacOS Sonoma, Windows, Linux]
References:
- Python Documentation: https://docs.python.org/3/
- Pygame Documentation: https://www.pygame.org/docs/
"""

class TicTacToe:
    def __init__(self, root):
        """
        Initialize the Tic-Tac-Toe game.

        Parameters:
            root (tk.Tk): The root window of the Tkinter application.
        """
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.current_player = "X"  # Player always starts as 'X'
        self.board = [""] * 9  # 3x3 board
        self.buttons = []
        self.player_score = 0
        self.ai_score = 0
        self.player_wins = 0
        self.ai_wins = 0
        self.ties = 0
        self.total_games = 0
        self.difficulty = "Easy"  # Default difficulty
        self.player_name = "Player"
        self.ai_name = "AI"
        self.game_mode = "Player vs AI"  # Default game mode
        self.ai_depth = 9  # Default depth for AI (for minimax)
        self.animation_speed = 100  # milliseconds
        self.setup_board()
        self.update_scores()
        self.setup_menu()
        self.configure_grid()

    def setup_board(self):
        """
        Set up the 3x3 grid of buttons representing the Tic-Tac-Toe board and the scoreboard.
        """
        # Create a 3x3 grid of buttons
        for i in range(9):
            button = tk.Button(
                self.root,
                text="",
                font=("Arial", 24),
                width=5,
                height=2,
                bg="light blue",
                command=partial(self.make_move, i),
            )
            button.grid(row=i // 3, column=i % 3, sticky="nsew", padx=5, pady=5)
            self.buttons.append(button)

        # Scoreboard
        self.score_label = tk.Label(
            self.root,
            text=self.get_score_text(),
            font=("Arial", 16),
            bg="light gray",
            relief="raised",
            bd=2,
        )
        self.score_label.grid(row=3, column=0, columnspan=3, sticky="nsew")

        # Statistics
        self.stats_label = tk.Label(
            self.root,
            text=self.get_stats_text(),
            font=("Arial", 12),
            bg="light gray",
            relief="sunken",
            bd=1,
        )
        self.stats_label.grid(row=4, column=0, columnspan=3, sticky="nsew")

    def setup_menu(self):
        """
        Set up the application menu with options for game modes, difficulty, resetting the game, and exiting.
        """
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)

        # Options Menu
        options_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options_menu)

        # Set Player Name
        options_menu.add_command(label="Set Player Name", command=self.set_player_name)

        # Game Mode Submenu
        game_mode_menu = tk.Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Game Mode", menu=game_mode_menu)
        game_mode_menu.add_command(label="Player vs AI", command=lambda: self.set_game_mode("Player vs AI"))
        game_mode_menu.add_command(label="Player vs Player", command=lambda: self.set_game_mode("Player vs Player"))
        game_mode_menu.add_command(label="AI vs AI", command=lambda: self.set_game_mode("AI vs AI"))

        # Difficulty Submenu
        difficulty_menu = tk.Menu(options_menu, tearoff=0)
        options_menu.add_cascade(label="Difficulty", menu=difficulty_menu)
        difficulty_menu.add_command(label="Easy", command=lambda: self.set_difficulty("Easy"))
        difficulty_menu.add_command(label="Medium", command=lambda: self.set_difficulty("Medium"))
        difficulty_menu.add_command(label="Hard", command=lambda: self.set_difficulty("Hard"))

        # Reset and Exit Options
        options_menu.add_separator()
        options_menu.add_command(label="Reset Game", command=self.reset_board)
        options_menu.add_command(label="Exit", command=self.root.quit)

    def configure_grid(self):
        """
        Configure the grid to make the GUI responsive.
        """
        for i in range(5):  # 0-4 rows
            self.root.rowconfigure(i, weight=1)
        for i in range(3):  # 0-2 columns
            self.root.columnconfigure(i, weight=1)

    def get_score_text(self):
        """
        Generate the scoreboard text.

        Returns:
            str: Formatted scoreboard text.
        """
        return f"{self.player_name}: {self.player_score}  {self.ai_name}: {self.ai_score}  Ties: {self.ties}"

    def get_stats_text(self):
        """
        Generate the statistics text.

        Returns:
            str: Formatted statistics text.
        """
        player_win_rate = (self.player_wins / self.total_games * 100) if self.total_games > 0 else 0
        ai_win_rate = (self.ai_wins / self.total_games * 100) if self.total_games > 0 else 0
        tie_rate = (self.ties / self.total_games * 100) if self.total_games > 0 else 0
        return (f"Total Games: {self.total_games} | "
                f"{self.player_name} Wins: {self.player_wins} ({player_win_rate:.1f}%) | "
                f"{self.ai_name} Wins: {self.ai_wins} ({ai_win_rate:.1f}%) | "
                f"Ties: {self.ties} ({tie_rate:.1f}%)")

    def set_player_name(self):
        """
        Prompt the user to enter their name.
        """
        name = simpledialog.askstring("Player Name", "Enter your name:", parent=self.root)
        if name:
            self.player_name = name
            self.update_scores()

    def set_game_mode(self, mode):
        """
        Set the game mode.

        Parameters:
            mode (str): The chosen game mode.
        """
        self.game_mode = mode
        messagebox.showinfo("Game Mode Changed", f"Game mode set to {mode}")
        self.reset_board()

    def set_difficulty(self, difficulty):
        """
        Set the AI difficulty level.

        Parameters:
            difficulty (str): The chosen difficulty level ("Easy", "Medium", "Hard").
        """
        self.difficulty = difficulty
        # Adjust AI depth based on difficulty
        if difficulty == "Easy":
            self.ai_depth = 1
        elif difficulty == "Medium":
            self.ai_depth = 3
        else:
            self.ai_depth = 9
        messagebox.showinfo("Difficulty Changed", f"AI Difficulty set to {difficulty}")
        self.reset_board()

    def update_scores(self):
        """
        Update the scoreboard and statistics with the current scores and statistics.
        """
        self.score_label.config(text=self.get_score_text())
        self.stats_label.config(text=self.get_stats_text())

    def make_move(self, index):
        """
        Handle the player's move at the specified board index.

        Parameters:
            index (int): The position on the board where the player wants to move.
        """
        if self.board[index] == "":
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player, state=tk.DISABLED)
            MOVE_SOUND.play()
            self.animate_move(index)
            if self.check_winner(self.current_player):
                self.handle_win(self.current_player)
            elif "" not in self.board:
                self.handle_tie()
            else:
                self.switch_player()
                if self.game_mode == "Player vs AI" and self.current_player == "O":
                    self.root.after(self.animation_speed, self.ai_move)
                elif self.game_mode == "AI vs AI" and self.current_player == "O":
                    self.root.after(self.animation_speed, self.ai_move)

    def animate_move(self, index):
        """
        Simple animation for a move by changing button color temporarily.

        Parameters:
            index (int): The position on the board that was moved.
        """
        original_color = self.buttons[index].cget("bg")
        self.buttons[index].config(bg="yellow")
        self.root.after(self.animation_speed, lambda: self.buttons[index].config(bg=original_color))

    def switch_player(self):
        """
        Switch the current player.
        """
        self.current_player = "O" if self.current_player == "X" else "X"

    def ai_move(self):
        """
        Determine and execute the AI's move based on the selected difficulty level.
        """
        if self.game_mode == "AI vs AI" and self.current_player == "O":
            # Disable user interaction during AI vs AI
            for button in self.buttons:
                button.config(state=tk.DISABLED)

        empty_indices = [i for i, x in enumerate(self.board) if x == ""]
        if not empty_indices:
            return

        if self.difficulty == "Easy":
            index = random.choice(empty_indices)
        elif self.difficulty == "Medium":
            index = self.block_player(empty_indices)
        else:  # Hard mode with minimax
            index = self.minimax_ai()

        self.board[index] = self.current_player
        self.buttons[index].config(text=self.current_player, state=tk.DISABLED)
        MOVE_SOUND.play()
        self.animate_move(index)

        if self.check_winner(self.current_player):
            self.handle_win(self.current_player)
        elif "" not in self.board:
            self.handle_tie()
        else:
            self.switch_player()
            if self.game_mode == "AI vs AI":
                self.root.after(self.animation_speed, self.ai_move)

    def block_player(self, empty_indices):
        """
        Attempt to block the player from winning by checking potential winning moves.

        Parameters:
            empty_indices (list): List of available board indices.

        Returns:
            int: The index to block the player's potential win or a random index if no block is needed.
        """
        for index in empty_indices:
            self.board[index] = "X"
            if self.check_winner("X"):
                self.board[index] = ""
                return index
            self.board[index] = ""
        return random.choice(empty_indices)

    def minimax_ai(self):
        """
        Implement the Minimax algorithm with alpha-beta pruning to determine the best move for the AI.

        Returns:
            int: The index of the optimal move.
        """
        best_score = -float('inf')
        best_move = None
        alpha = -float('inf')
        beta = float('inf')

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(False, alpha, beta, 1)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_move if best_move is not None else random.choice([i for i, x in enumerate(self.board) if x == ""])

    def minimax(self, is_maximizing, alpha, beta, depth):
        """
        Recursive Minimax function with alpha-beta pruning.

        Parameters:
            is_maximizing (bool): Flag indicating whether the current move is maximizing or minimizing.
            alpha (float): The best already explored option along the path to the root for the maximizer.
            beta (float): The best already explored option along the path to the root for the minimizer.
            depth (int): Current depth of the recursion.

        Returns:
            int: The score of the board.
        """
        if self.check_winner("O"):
            return 1
        elif self.check_winner("X"):
            return -1
        elif "" not in self.board:
            return 0

        if depth >= self.ai_depth:
            return 0  # Neutral score for depth limit

        if is_maximizing:
            max_eval = -float('inf')
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "O"
                    eval = self.minimax(False, alpha, beta, depth + 1)
                    self.board[i] = ""
                    max_eval = max(eval, max_eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "X"
                    eval = self.minimax(True, alpha, beta, depth + 1)
                    self.board[i] = ""
                    min_eval = min(eval, min_eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def check_winner(self, player):
        """
        Check if the specified player has won the game.

        Parameters:
            player (str): The player symbol ("X" or "O").

        Returns:
            bool: True if the player has won, False otherwise.
        """
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
            if all(self.board[i] == player for i in combo):
                for i in combo:
                    self.buttons[i].config(bg="light green")
                return True
        return False

    def handle_win(self, winner):
        """
        Handle the event when a player or AI wins the game.

        Parameters:
            winner (str): The symbol of the winner ("X" or "O").
        """
        WIN_SOUND.play()
        self.total_games += 1
        if winner == "X":
            self.player_score += 1
            self.player_wins += 1
            message = f"{self.player_name} wins!"
        else:
            self.ai_score += 1
            self.ai_wins += 1
            message = f"{self.ai_name} wins!"
        self.update_scores()
        messagebox.showinfo("Game Over", message)
        self.reset_board(highlight=False)

    def handle_tie(self):
        """
        Handle the event when the game ends in a tie.
        """
        TIE_SOUND.play()
        self.ties += 1
        self.total_games += 1
        self.update_scores()
        messagebox.showinfo("Game Over", "It's a tie!")
        self.reset_board(highlight=False)

    def end_game(self, message):
        """
        Handle the end of the game by displaying a message and resetting the board.

        Parameters:
            message (str): The message to display to the user.
        """
        messagebox.showinfo("Game Over", message)
        self.reset_board()

    def reset_board(self, highlight=True):
        """
        Reset the game board for a new game.

        Parameters:
            highlight (bool): Whether to reset the scores. Defaults to True.
        """
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL, bg="light blue")
        self.current_player = "X"
        if highlight:
            self.update_scores()
        # If AI vs AI, start the game automatically
        if self.game_mode == "AI vs AI" and self.current_player == "O":
            self.root.after(self.animation_speed, self.ai_move)

    def play_ai_vs_ai(self):
        """
        Automatically play AI vs AI games.
        """
        if self.game_mode == "AI vs AI" and self.current_player == "O":
            self.ai_move()

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    # Set minimum size for better responsiveness
    root.minsize(300, 400)
    # Create the game instance
    game = TicTacToe(root)
    # Start the Tkinter event loop
    root.mainloop()
