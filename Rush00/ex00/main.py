import sys
from checkmate import checkmate

def validate_board(board_str):
    board = [line.strip().upper() for line in board_str.strip().split('\n') if line.strip()]

    if not board:
        print("Error: Board is empty.")
        sys.exit(1)

    size = len(board)

    if not (1 <= size <= 100):
        print(f"Error: Board size {size} is out of range (1-100).")
        sys.exit(1)

    counts = {'K': 0, 'Q': 0, 'R': 0, 'B': 0, 'P': 0}
    valid_chars = {'K', 'Q', 'R', 'B', 'P', '.'}

    for i, row in enumerate(board):
        if len(row) != size:
            print(f"Error: Row {i+1} length is {len(row)}, expected {size}.")
            sys.exit(1)
        for char in row:
            if char not in valid_chars:
                print(f"Error: Invalid piece '{char}' at row {i+1}.")
                sys.exit(1)
            if char in counts:
                counts[char] += 1

    if counts['K'] != 1:
        print(f"Error: King (K) count is {counts['K']}, must be 1.")
        sys.exit(1)
    if counts['Q'] > 1:
        print(f"Error: Queen (Q) count is {counts['Q']}, max is 1.")
        sys.exit(1)
    if counts['R'] > 2:
        print(f"Error: Rook (R) count is {counts['R']}, max is 2.")
        sys.exit(1)
    if counts['B'] > 2:
        print(f"Error: Bishop (B) count is {counts['B']}, max is 2.")
        sys.exit(1)
    if counts['P'] > size:
        print(f"Error: Pawn (P) count is {counts['P']}, max for this size is {size}.")
        sys.exit(1)

    return board

def main():
    board1 = """\
R...
.K..
..P.
....\

"""
    board2 = """\
..P.
.K..
....
..K.\
"""
    board = validate_board(board2)
    checkmate(board)

if __name__ == "__main__":
    main()