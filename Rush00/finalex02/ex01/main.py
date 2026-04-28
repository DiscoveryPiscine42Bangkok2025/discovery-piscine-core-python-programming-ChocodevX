import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from validator import validate_board, parse_board_from_lines
from checkmate import is_in_check, get_attackers

app = Flask(__name__)
CORS(app)

@app.route('/api/check', methods=['POST'])
def api_check():
    try:
        data = request.get_json(force=True)

        if 'raw' in data:
            lines = [l for l in data['raw'].splitlines() if l.strip()]
            board, size = parse_board_from_lines(lines)
        elif 'board' in data:
            board = [r.upper() for r in data['board']]
            size = len(board)
        else:
            return jsonify({"error": "Provide 'board' array or 'raw' text."}), 400

        # ตรวจสอบความถูกต้องของหมาก
        validate_board(board, size)
        
        # ประมวลผล Logic การ Check
        result = is_in_check(board)
        attackers = get_attackers(board) if result else []

        return jsonify({
            "result": "Success" if result else "Fail",
            "in_check": result,
            "attackers": attackers,
            "board": board,
            "size": size,
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # กำหนด Port เริ่มต้นที่ 5000
    port = 5555
    print(f"🚀 Chess Check API running → http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)