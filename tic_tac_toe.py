# The board is now defined inside the main loop to ensure it resets.
def print_board(board):
    """Prints the Tic-Tac-Toe board to the console."""
    print() # Add a blank line for spacing
    print(f" {board[0]} | {board[1]} | {board[2]}    (1 | 2 | 3)")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}    (4 | 5 | 6)")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}    (7 | 8 | 9)")
    print()

def check_win(board, player):
    """Checks if the given player has won the game."""
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]             # Diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player:
            return True
    return False

def check_draw(board):
    """Checks if the game is a draw (board is full)."""
    return ' ' not in board

def play_game():
    """Runs a single round of Tic-Tac-Toe."""
    # Reset the board for a new game
    board = [' ' for _ in range(9)]
    current_player = 'X'
    
    while True:
        print_board(board)
        print(f"Player {current_player}'s turn.")

        try:
            move_str = input("Choose a spot (1-9): ")
            if not move_str: # Handle empty input
                print("⚠️ Please enter a number.")
                continue

            move = int(move_str)

            if not 1 <= move <= 9:
                print("⚠️ Invalid number. Please choose between 1 and 9.")
                continue
            if board[move - 1] != ' ':
                print("🚫 That spot is already taken! Choose another one.")
                continue

            board[move - 1] = current_player

            if check_win(board, current_player):
                print_board(board)
                print(f"🎉 Congratulations! Player {current_player} wins! 🎉")
                return # End this game round

            if check_draw(board):
                print_board(board)
                print("🤝 It's a draw! 🤝")
                return # End this game round
            
            # Switch players
            current_player = 'O' if current_player == 'X' else 'X'

        except ValueError:
            print("⚠️ Invalid input. Please enter a number from 1 to 9.")

# Main function to control the game and the "Play Again" loop
def main():
    """Main entry point of the script."""
    print("Welcome to Tic-Tac-Toe! 🕹️")
    while True:
        play_game()
        
        while True:
            play_again = input("Play again? (yes/no): ").lower().strip()
            if play_again in ["yes", "no"]:
                break
            print("Invalid input. Please enter 'yes' or 'no'.")
        
        if play_again == "no":
            print("Thanks for playing! 👋")
            break

# This makes sure the script runs the main function
if __name__ == "__main__":
    main()
