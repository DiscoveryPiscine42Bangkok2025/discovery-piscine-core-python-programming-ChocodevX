Board = list[str]

# ── Direction sets ─────────────────────────────────────────────────────────────

_STRAIGHT   = [(-1, 0), (1, 0), (0, -1), (0, 1)]
_DIAGONAL   = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
_KNIGHT_HOP = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
_PAWN_ATTACK = [(-1, -1), (-1, 1)]

# ── Helpers ────────────────────────────────────────────────────────────────────

def _find_king(board: Board) -> tuple[int, int]:
    size = len(board)
    for r in range(size):
        for c in range(size):
            if board[r][c] == "K":
                return (r, c)
    raise ValueError("King (K) not found.")


def _in_bounds(r: int, c: int, size: int) -> bool:
    return 0 <= r < size and 0 <= c < size


def _slide_attackers(board: Board, size: int, kr: int, kc: int,
                     directions: list[tuple[int, int]], pieces: str) -> list[dict]:
    """Collect sliding attackers (rook/bishop/queen) along the given directions."""
    attackers = []
    for dr, dc in directions:
        r, c, path = kr + dr, kc + dc, []
        while _in_bounds(r, c, size):
            if board[r][c] != ".":
                if board[r][c] in pieces:
                    attackers.append({"piece": board[r][c], "row": r, "col": c,
                                      "path": path[:], "type": "slide"})
                break
            path.append((r, c))
            r, c = r + dr, c + dc
    return attackers


def _hop_attackers(board: Board, size: int, kr: int, kc: int,
                   hops: list[tuple[int, int]], pieces: str, kind: str) -> list[dict]:
    """Collect non-sliding attackers (knight / pawn)."""
    return [
        {"piece": board[r][c], "row": r, "col": c, "path": [], "type": kind}
        for dr, dc in hops
        if _in_bounds(r := kr + dr, c := kc + dc, size) and board[r][c] in pieces
    ]

# ── Public API ─────────────────────────────────────────────────────────────────

def get_attackers(board: Board) -> list[dict]:
    size = len(board)
    kr, kc = _find_king(board)
    return (
        _slide_attackers(board, size, kr, kc, _STRAIGHT, "RQ") +
        _slide_attackers(board, size, kr, kc, _DIAGONAL, "BQ") +
        _hop_attackers(board, size, kr, kc, _KNIGHT_HOP, "N", "knight") +
        _hop_attackers(board, size, kr, kc, _PAWN_ATTACK, "P", "pawn")
    )


def is_in_check(board: Board) -> bool:
    return bool(get_attackers(board))
