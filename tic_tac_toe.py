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

