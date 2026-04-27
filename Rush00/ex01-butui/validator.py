"""
validator.py — ตรวจสอบความถูกต้องของ board สำหรับ Web API
"""

VALID_PIECES = {'K', 'Q', 'R', 'B', 'N', 'P', '.'}

PIECE_LIMITS = {
    'K': (1, 1),   # ต้องมีพอดี 1
    'Q': (0, 1),   # มีได้ไม่เกิน 1
    'R': (0, 2),
    'B': (0, 2),
    'N': (0, 2),
    'P': (0, None),
}

def validate_board(board: list[str], size: int) -> list[str]:
    """
    ตรวจสอบ board และ raise ValueError เมื่อพบข้อผิดพลาด
    """
    errors = []

    if len(board) != size:
        errors.append(f"Board must have {size} rows, got {len(board)}.")

    counts = {p: 0 for p in PIECE_LIMITS}

    for i, row in enumerate(board):
        if len(row) != size:
            errors.append(f"Row {i+1}: length {len(row)}, expected {size}.")

        for ch in row:
            if ch not in VALID_PIECES:
                errors.append(f"Row {i+1}: invalid character '{ch}'.")
            elif ch in counts:
                counts[ch] += 1

    for piece, (min_count, max_count) in PIECE_LIMITS.items():
        actual = counts[piece]
        effective_max = size if max_count is None else max_count

        if actual < min_count:
            errors.append(f"Piece '{piece}': need {min_count}, found {actual}.")
        if actual > effective_max:
            errors.append(f"Piece '{piece}': max {effective_max}, found {actual}.")

    if errors:
        raise ValueError(" | ".join(errors))

    return board

def parse_board_from_lines(lines: list[str]) -> tuple[list[str], int]:
    if not lines:
        raise ValueError("Input is empty.")

    first = lines[0].replace("num", "").replace("=", "").strip()
    if first.isdigit():
        size = int(first)
        board = [r.upper() for r in lines[1:]]
    else:
        size = len(lines[0].strip())
        board = [r.upper() for r in lines]

    return board, size