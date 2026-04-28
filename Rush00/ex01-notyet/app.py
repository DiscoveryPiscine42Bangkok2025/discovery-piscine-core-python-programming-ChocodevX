from flask import Flask, request, jsonify
from flask_cors import CORS
import chess
import chess.engine
import math

app = Flask(__name__)
CORS(app)

# ─── Piece values ───────────────────────────────────────────────────────────
PIECE_VALUE = {
    chess.PAWN: 100, chess.KNIGHT: 320, chess.BISHOP: 330,
    chess.ROOK: 500, chess.QUEEN: 900, chess.KING: 20000,
}

# Piece-square tables (from white's perspective, rank 1→8 bottom→top)
PST = {
    chess.PAWN: [
         0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
         5,  5, 10, 25, 25, 10,  5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5, -5,-10,  0,  0,-10, -5,  5,
         5, 10, 10,-20,-20, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0,
    ],
    chess.KNIGHT: [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50,
    ],
    chess.BISHOP: [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20,
    ],
    chess.ROOK: [
         0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         0,  0,  0,  5,  5,  0,  0,  0,
    ],
    chess.QUEEN: [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20,
    ],
    chess.KING: [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
         20, 20,  0,  0,  0,  0, 20, 20,
         20, 30, 10,  0,  0, 10, 30, 20,
    ],
}


def evaluate(board: chess.Board) -> int:
    if board.is_checkmate():
        return -20000 if board.turn == chess.WHITE else 20000
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    score = 0
    for sq in chess.SQUARES:
        piece = board.piece_at(sq)
        if not piece:
            continue
        val = PIECE_VALUE[piece.piece_type]
        # PST: white uses square index as-is (a1=0), black mirrors vertically
        idx = sq if piece.color == chess.WHITE else chess.square_mirror(sq)
        pst_val = PST[piece.piece_type][idx]
        total = val + pst_val
        score += total if piece.color == chess.WHITE else -total
    return score


def order_moves(board: chess.Board):
    """Simple move ordering: captures first."""
    moves = list(board.legal_moves)
    def priority(m):
        if board.is_capture(m):
            victim = board.piece_at(m.to_square)
            attacker = board.piece_at(m.from_square)
            if victim and attacker:
                return -(PIECE_VALUE[victim.piece_type] - PIECE_VALUE[attacker.piece_type])
        return 0
    moves.sort(key=priority)
    return moves


def minimax(board: chess.Board, depth: int, alpha: int, beta: int, maximizing: bool) -> int:
    if depth == 0 or board.is_game_over():
        return evaluate(board)

    if maximizing:
        best = -math.inf
        for move in order_moves(board):
            board.push(move)
            best = max(best, minimax(board, depth - 1, alpha, beta, False))
            board.pop()
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = math.inf
        for move in order_moves(board):
            board.push(move)
            best = min(best, minimax(board, depth - 1, alpha, beta, True))
            board.pop()
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def find_best_move(board: chess.Board, depth: int = 3) -> chess.Move | None:
    best_move, best_score = None, -math.inf if board.turn == chess.WHITE else math.inf
    maximizing = board.turn == chess.WHITE

    for move in order_moves(board):
        board.push(move)
        score = minimax(board, depth - 1, -math.inf, math.inf, not maximizing)
        board.pop()
        if maximizing and score > best_score:
            best_score, best_move = score, move
        elif not maximizing and score < best_score:
            best_score, best_move = score, move

    return best_move


def board_to_grid(board: chess.Board) -> list[str]:
    """Convert python-chess board to list of 8 strings (rank 8 → rank 1)."""
    rows = []
    for rank in range(7, -1, -1):
        row = ""
        for file in range(8):
            sq = chess.square(file, rank)
            p = board.piece_at(sq)
            row += p.symbol().upper() if p else "."
        rows.append(row)
    return rows


def get_check_info(board: chess.Board) -> dict:
    in_check = board.is_check()
    attackers_info = []
    if in_check:
        king_sq = board.king(board.turn)
        kr, kc = chess.square_rank(king_sq), chess.square_file(king_sq)
        # frontend row 0 = rank 7
        king_row = 7 - kr

        for sq in board.attackers(not board.turn, king_sq):
            p = board.piece_at(sq)
            ar, ac = chess.square_rank(sq), chess.square_file(sq)
            attackers_info.append({
                "piece": p.symbol().upper() if p else "?",
                "row": 7 - ar,
                "col": ac,
                "path": [],
                "type": "attack",
            })
    return {"in_check": in_check, "attackers": attackers_info}


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/api/new", methods=["POST"])
def api_new():
    """Start a new game, optionally from a FEN."""
    data = request.get_json(force=True) or {}
    fen = data.get("fen", chess.STARTING_FEN)
    try:
        board = chess.Board(fen)
    except Exception:
        return jsonify({"error": "Invalid FEN"}), 400

    check = get_check_info(board)
    return jsonify({
        "fen": board.fen(),
        "board": board_to_grid(board),
        "turn": "white" if board.turn == chess.WHITE else "black",
        "legal_moves": [m.uci() for m in board.legal_moves],
        "status": _game_status(board),
        **check,
    })


@app.route("/api/move", methods=["POST"])
def api_move():
    """Apply a move (UCI string) to a FEN position."""
    data = request.get_json(force=True) or {}
    fen = data.get("fen")
    uci = data.get("move")
    if not fen or not uci:
        return jsonify({"error": "Provide 'fen' and 'move' (UCI)."}), 400

    try:
        board = chess.Board(fen)
        move = chess.Move.from_uci(uci)
        if move not in board.legal_moves:
            return jsonify({"error": "Illegal move."}), 400
        board.push(move)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    check = get_check_info(board)
    return jsonify({
        "fen": board.fen(),
        "board": board_to_grid(board),
        "turn": "white" if board.turn == chess.WHITE else "black",
        "legal_moves": [m.uci() for m in board.legal_moves],
        "last_move": uci,
        "status": _game_status(board),
        **check,
    })


@app.route("/api/best-move", methods=["POST"])
def api_best_move():
    """Return the best move for the current position."""
    data = request.get_json(force=True) or {}
    fen = data.get("fen")
    depth = min(int(data.get("depth", 3)), 5)   # cap depth at 5 for speed
    if not fen:
        return jsonify({"error": "Provide 'fen'."}), 400

    try:
        board = chess.Board(fen)
    except Exception:
        return jsonify({"error": "Invalid FEN"}), 400

    if board.is_game_over():
        return jsonify({"error": "Game is already over."}), 400

    move = find_best_move(board, depth)
    if not move:
        return jsonify({"error": "No legal moves."}), 400

    board.push(move)
    check = get_check_info(board)
    return jsonify({
        "best_move": move.uci(),
        "fen": board.fen(),
        "board": board_to_grid(board),
        "turn": "white" if board.turn == chess.WHITE else "black",
        "legal_moves": [m.uci() for m in board.legal_moves],
        "status": _game_status(board),
        **check,
    })


@app.route("/api/check", methods=["POST"])
def api_check():
    """Legacy: check if King is in check from a board array."""
    data = request.get_json(force=True) or {}
    fen = data.get("fen")
    if fen:
        try:
            board = chess.Board(fen)
        except Exception:
            return jsonify({"error": "Invalid FEN"}), 400
    elif "board" in data:
        # Reconstruct FEN from 8-row grid (white pieces uppercase, black lowercase not supported here)
        rows = [r.upper() for r in data["board"]]
        fen_rows = []
        for row in rows:
            fen_row, empty = "", 0
            for ch in row:
                if ch == ".":
                    empty += 1
                else:
                    if empty:
                        fen_row += str(empty)
                        empty = 0
                    fen_row += ch
            if empty:
                fen_row += str(empty)
            fen_rows.append(fen_row)
        fen = "/".join(fen_rows) + " w - - 0 1"
        try:
            board = chess.Board(fen)
        except Exception as e:
            return jsonify({"error": f"Invalid board: {e}"}), 400
    else:
        return jsonify({"error": "Provide 'fen' or 'board'."}), 400

    check = get_check_info(board)
    return jsonify({
        "result": "Success" if check["in_check"] else "Fail",
        "board": board_to_grid(board),
        **check,
    })


def _game_status(board: chess.Board) -> str:
    if board.is_checkmate():
        return "checkmate"
    if board.is_stalemate():
        return "stalemate"
    if board.is_insufficient_material():
        return "draw_material"
    if board.is_seventyfive_moves():
        return "draw_75"
    if board.is_fivefold_repetition():
        return "draw_repetition"
    if board.is_check():
        return "check"
    return "ongoing"


if __name__ == "__main__":
    port = 5000
    print(f"♟  Chess API → http://localhost:{port}")
    print("  POST /api/new        – start game (optional: fen)")
    print("  POST /api/move       – apply move (fen + move UCI)")
    print("  POST /api/best-move  – AI best move (fen, depth 1-5)")
    print("  POST /api/check      – legacy check detector")
    app.run(host="0.0.0.0", port=port, debug=True)
