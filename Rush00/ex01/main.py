import sys
import os
from checkmate import checkmate

def validate_board(board, size):
    if not board or len(board) != size:
        print(f"Error: Board must have exactly {size} rows.")
        sys.exit(1)

    # Dictionary เก็บจำนวนตัวหมาก
    counts = {'K': 0, 'Q': 0, 'R': 0, 'B': 0, 'P': 0}
    valid_chars = {'K', 'Q', 'R', 'B', 'P', '.'}

    for i, row in enumerate(board):
        # ตรวจสอบความยาวแถว (ห้ามแหว่ง ห้ามขาด ห้ามเกิน)
        if len(row) != size:
            print(f"Error: Row {i+1} length is {len(row)}, expected {size}.")
            sys.exit(1)
        
        for char in row:
            if char not in valid_chars:
                print(f"Error: Invalid piece '{char}' at row {i+1}.")
                sys.exit(1)
            if char in counts:
                counts[char] += 1

    # --- ตรวจสอบ Limit ตามเงื่อนไขที่คุณระบุ ---
    # 1. King ต้องมี 1 ตัวเท่านั้น
    if counts['K'] != 1:
        print(f"Error: King (K) count is {counts['K']}, must be 1.")
        sys.exit(1)

    # 2. Queen มีได้แค่ 1 ตัว
    if counts['Q'] > 1:
        print(f"Error: Queen (Q) count is {counts['Q']}, max allowed is 1.")
        sys.exit(1)

    # 3. Bishop และ Rook อย่างละไม่เกิน 2
    if counts['R'] > 2:
        print(f"Error: Rook (R) count is {counts['R']}, max allowed is 2.")
        sys.exit(1)
    if counts['B'] > 2:
        print(f"Error: Bishop (B) count is {counts['B']}, max allowed is 2.")
        sys.exit(1)

    # 4. Pawn มีได้ไม่เกินขนาดของตาราง (size)
    if counts['P'] > size:
        print(f"Error: Pawn (P) count is {counts['P']}, max for size {size} is {size}.")
        sys.exit(1)
    
    return True

def handle_manual_input():
    try:
        size_str = input("Enter board size (1-100): ").strip()
        if not size_str.isdigit():
            print("Error: Size must be a positive integer.")
            sys.exit(1)
        size = int(size_str)
        if not (1 <= size <= 100):
            print("Error: Size must be 1-100.")
            sys.exit(1)

        print(f"Input {size} rows (Length {size} each):")
        board = []
        for i in range(size):
            row = input(f"Row {i+1}: ").strip().upper()
            board.append(row)
        return board, size
    except (EOFError, KeyboardInterrupt):
        sys.exit(1)

def handle_file_input(filename):
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    try:
        with open(filename, 'r') as f:
            lines = [l.strip() for l in f if l.strip()]
        if not lines:
            sys.exit(1)

        first_line = lines[0].replace("num", "").replace("=", "").strip()
        if first_line.isdigit():
            size = int(first_line)
            board = [r.upper() for r in lines[1:]]
        else:
            size = len(lines[0])
            board = [r.upper() for r in lines]
        return board, size
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    if len(sys.argv) == 2:
        board, size = handle_file_input(sys.argv[1])
    else:
        board, size = handle_manual_input()

    if validate_board(board, size):
        checkmate(board)

if __name__ == "__main__":
    main()