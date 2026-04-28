import sys
import chess
from flask import Flask, request, jsonify
from flask_cors import CORS
from bot import get_best_move

app = Flask(__name__)
CORS(app)

# ── Helpers ────────────────────────────────────────────────────────────────────

def board_response(board: chess.Board, **extra) -> dict:
    return {
        "fen": board.fen(),
        "is_game_over": board.is_game_over(),
        "result": board.result() if board.is_game_over() else None,
        "is_check": board.is_check(),
        **extra,
    }


def promote_if_needed(board: chess.Board, uci: str) -> str:
    """Auto-promote pawn to queen when no promotion piece is specified."""
    move = chess.Move.from_uci(uci)
    piece = board.piece_at(move.from_square)
    if (
        piece and piece.piece_type == chess.PAWN
        and chess.square_rank(move.to_square) in (0, 7)
        and len(uci) == 4
    ):
        uci += "q"
    return uci

# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route("/api/game/new", methods=["GET"])
def game_new():
    board = chess.Board()
    return jsonify(board_response(board))


@app.route("/api/game/legal_moves", methods=["POST"])
def game_legal_moves():
    data = request.get_json(force=True)
    fen, square_name = data.get("fen"), data.get("square")
    if not fen or not square_name:
        return jsonify({"error": "Missing 'fen' or 'square'"}), 400

    try:
        board = chess.Board(fen)
        sq = chess.parse_square(square_name)
        moves = [chess.square_name(m.to_square) for m in board.legal_moves if m.from_square == sq]
        return jsonify({"legal_moves": moves})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/game/move", methods=["POST"])
def game_move():
    data = request.get_json(force=True)
    fen, uci = data.get("fen"), data.get("move")

    try:
        board = chess.Board(fen)
        uci = promote_if_needed(board, uci)
        move = chess.Move.from_uci(uci)

        if move not in board.legal_moves:
            return jsonify({"valid": False, "error": "Illegal move"}), 400

        board.push(move)
        return jsonify({"valid": True, **board_response(board)})
    except Exception as e:
        return jsonify({"valid": False, "error": str(e)}), 400


@app.route("/api/game/bot", methods=["POST"])
def game_bot():
    data = request.get_json(force=True)
    fen = data.get("fen")

    try:
        board = chess.Board(fen)
        if board.is_game_over():
            return jsonify({"error": "Game is already over"}), 400

        bot_uci = get_best_move(board)
        if not bot_uci:
            return jsonify({"error": "Bot cannot make a move"}), 500

        board.push(chess.Move.from_uci(bot_uci))
        return jsonify({"bot_move": bot_uci, **board_response(board)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# ── Entry point ────────────────────────────────────────────────────────────────

def parse_port() -> int:
    try:
        idx = sys.argv.index("--port")
        return int(sys.argv[idx + 1])
    except (ValueError, IndexError):
        return 5000


if __name__ == "__main__":
    port = parse_port()
    print(f"🚀 Chess API → http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=True)
