"""validator.py — ตรวจสอบความถูกต้องของ board"""

VALID_PIECES = {"K", "Q", "R", "B", "N", "P", "."}

# (min, max) — None หมายถึงใช้ขนาด board เป็น max
PIECE_LIMITS: dict[str, tuple[int, int | None]] = {
    "K": (1, 1),
    "Q": (0, 1),
    "R": (0, 2),
    "B": (0, 2),
    "N": (0, 2),
    "P": (0, None),
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def _count_pieces(board: list[str]) -> dict[str, int]:
    counts = {p: 0 for p in PIECE_LIMITS}
    for row in board:
        for ch in row:
            if ch in counts:
                counts[ch] += 1
    return counts


def _check_shape(board: list[str], size: int) -> list[str]:
    errors = []
    if len(board) != size:
        errors.append(f"Board must have {size} rows, got {len(board)}.")
    for i, row in enumerate(board):
        if len(row) != size:
            errors.append(f"Row {i + 1}: length {len(row)}, expected {size}.")
        for ch in row:
            if ch not in VALID_PIECES:
                errors.append(f"Row {i + 1}: invalid character '{ch}'.")
    return errors


def _check_counts(counts: dict[str, int], size: int) -> list[str]:
    errors = []
    for piece, (lo, hi) in PIECE_LIMITS.items():
        actual = counts[piece]
        effective_hi = size if hi is None else hi
        if actual < lo:
            errors.append(f"Piece '{piece}': need {lo}, found {actual}.")
        if actual > effective_hi:
            errors.append(f"Piece '{piece}': max {effective_hi}, found {actual}.")
    return errors

# ── Public API ─────────────────────────────────────────────────────────────────

def validate_board(board: list[str], size: int) -> list[str]:
    errors = _check_shape(board, size) + _check_counts(_count_pieces(board), size)
    if errors:
        raise ValueError(" | ".join(errors))
    return board


def parse_board_from_lines(lines: list[str]) -> tuple[list[str], int]:
    if not lines:
        raise ValueError("Input is empty.")

    header = lines[0].replace("num", "").replace("=", "").strip()
    if header.isdigit():
        size = int(header)
        board = [r.upper() for r in lines[1:]]
    else:
        size = len(lines[0].strip())
        board = [r.upper() for r in lines]

    return board, size
