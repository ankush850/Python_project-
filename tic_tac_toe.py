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
