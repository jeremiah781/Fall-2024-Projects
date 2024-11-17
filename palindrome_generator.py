import random

# Display the board
def display_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")

# Check for a win
def check_winner(board, player):
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combination in win_combinations:
        if all(board[pos] == player for pos in combination):
            return True
    return False

# Check for a tie
def check_tie(board):
    return all(pos != " " for pos in board)

# Player move
def player_move(board, player):
    while True:
        try:
            move = int(input(f"Player {player}, enter your move (1-9): ")) - 1
            if board[move] == " ":
                board[move] = player
                break
            else:
                print("Spot already taken. Try again.")
        except (IndexError, ValueError):
            print("Invalid input. Enter a number between 1 and 9.")

# Easy AI (random moves)
def ai_easy_move(board, ai_player):
    print("AI is making its move (Easy)...")
    empty_positions = [i for i in range(9) if board[i] == " "]
    board[random.choice(empty_positions)] = ai_player

# Medium AI (basic strategy)
def ai_medium_move(board, ai_player, human_player):
    print("AI is making its move (Medium)...")

    # Check if AI can win
    for move in range(9):
        if board[move] == " ":
            board[move] = ai_player
            if check_winner(board, ai_player):
                return
            board[move] = " "  # Undo move

    # Check if AI needs to block the player
    for move in range(9):
        if board[move] == " ":
            board[move] = human_player
            if check_winner(board, human_player):
                board[move] = ai_player
                return
            board[move] = " "  # Undo move

    # Choose the center
    if board[4] == " ":
        board[4] = ai_player
        return

    # Choose a corner
    for move in [0, 2, 6, 8]:
        if board[move] == " ":
            board[move] = ai_player
            return

    # Choose any remaining spot
    for move in range(9):
        if board[move] == " ":
            board[move] = ai_player
            return

# Hard AI (advanced strategy)
def ai_hard_move(board, ai_player, human_player):
    print("AI is making its move (Hard)...")
    ai_medium_move(board, ai_player, human_player)  # Full strategy for now

# AI move based on difficulty
def ai_move(board, ai_player, human_player, difficulty):
    if difficulty == "Easy":
        ai_easy_move(board, ai_player)
    elif difficulty == "Medium":
        ai_medium_move(board, ai_player, human_player)
    elif difficulty == "Hard":
        ai_hard_move(board, ai_player, human_player)

# Main game loop
def play_game():
    print("Welcome to Tic-Tac-Toe!")
    print("You can play against AI or another player.")
    mode = input("Enter '1' for Player vs Player or '2' for Player vs AI: ")

    difficulty = "Easy"  # Default difficulty
    if mode == "2":
        difficulty = input("Choose difficulty (Easy, Medium, Hard): ").capitalize()

    board = [" "] * 9
    current_player = "X"

    display_board(board)

    while True:
        if mode == "2" and current_player == "O":
            ai_move(board, "O", "X", difficulty)
        else:
            player_move(board, current_player)

        display_board(board)

        if check_winner(board, current_player):
            if mode == "2" and current_player == "O":
                print("AI wins! Better luck next time.")
            else:
                print(f"Player {current_player} wins!")
            break
        elif check_tie(board):
            print("It's a tie!")
            break

        # Switch player
        current_player = "O" if current_player == "X" else "X"

# Run the game
if __name__ == "__main__":
    play_game()
