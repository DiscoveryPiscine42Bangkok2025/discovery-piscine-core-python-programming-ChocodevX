import chess

# ── Constants ──────────────────────────────────────────────────────────────────

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000,
}

KNIGHT_TABLE = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,   0,   0,   0,   0, -20, -40,
    -30,   0,  10,  15,  15,  10,   0, -30,
    -30,   5,  15,  20,  20,  15,   5, -30,
    -30,   0,  15,  20,  20,  15,   0, -30,
    -30,   5,  10,  15,  15,  10,   5, -30,
    -40, -20,   0,   5,   5,   0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50,
]

SEARCH_DEPTH = 3
INF = 999999

# ── Evaluation ─────────────────────────────────────────────────────────────────

def piece_score(piece: chess.Piece, square: int) -> int:
    value = PIECE_VALUES.get(piece.piece_type, 0)
    if piece.piece_type == chess.KNIGHT:
        idx = square if piece.color == chess.WHITE else chess.square_mirror(square)
        value += KNIGHT_TABLE[idx]
    return value if piece.color == chess.WHITE else -value


def evaluate(board: chess.Board) -> int:
    if board.is_checkmate():
        return -INF if board.turn == chess.WHITE else INF
    return sum(
        piece_score(piece, sq)
        for sq in chess.SQUARES
        if (piece := board.piece_at(sq))
    )

# ── Search ─────────────────────────────────────────────────────────────────────

def minimax(board: chess.Board, depth: int, alpha: int, beta: int, maximizing: bool) -> int:
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    best = -INF if maximizing else INF
    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth - 1, alpha, beta, not maximizing)
        board.pop()

        if maximizing:
            best = max(best, score)
            alpha = max(alpha, score)
        else:
            best = min(best, score)
            beta = min(beta, score)

        if beta <= alpha:
            break

    return best


def get_best_move(board: chess.Board) -> str | None:
    best_move, best_score = None, -INF

    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, SEARCH_DEPTH - 1, -INF, INF, False)
        board.pop()

        if score > best_score:
            best_score, best_move = score, move

    return best_move.uci() if best_move else None
