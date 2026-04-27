def is_in_check(board: list[str]) -> bool:
    size = len(board)
    king_pos = _find_king(board, size)
    if not king_pos: raise ValueError("King (K) not found.")
    kr, kc = king_pos
    return (_check_straight(board, size, kr, kc) or 
            _check_diagonal(board, size, kr, kc) or 
            _check_knight(board, size, kr, kc) or 
            _check_pawn(board, size, kr, kc))

def get_attackers(board: list[str]) -> list[dict]:
    size = len(board)
    king_pos = _find_king(board, size)
    if not king_pos: return []
    kr, kc = king_pos
    attackers = []
    
    # Straight (R/Q)
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        r, c, path = kr+dr, kc+dc, []
        while 0 <= r < size and 0 <= c < size:
            if board[r][c] != '.':
                if board[r][c] in 'RQ': attackers.append({"piece":board[r][c],"row":r,"col":c,"path":path[:],"type":"straight"})
                break
            path.append((r,c))
            r, c = r+dr, c+dc
            
    # Diagonal (B/Q)
    for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
        r, c, path = kr+dr, kc+dc, []
        while 0 <= r < size and 0 <= c < size:
            if board[r][c] != '.':
                if board[r][c] in 'BQ': attackers.append({"piece":board[r][c],"row":r,"col":c,"path":path[:],"type":"diagonal"})
                break
            path.append((r,c))
            r, c = r+dr, c+dc

    # Knight (N)
    for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        r, c = kr+dr, kc+dc
        if 0 <= r < size and 0 <= c < size and board[r][c] == 'N':
            attackers.append({"piece":"N","row":r,"col":c,"path":[],"type":"knight"})

    # Pawn (P)
    for dr, dc in [(-1,-1),(-1,1)]:
        r, c = kr+dr, kc+dc
        if 0 <= r < size and 0 <= c < size and board[r][c] == 'P':
            attackers.append({"piece":"P","row":r,"col":c,"path":[],"type":"pawn"})
            
    return attackers

def _find_king(board, size):
    for r in range(size):
        for c in range(size):
            if board[r][c] == 'K': return (r, c)
    return None

def _check_straight(board, size, kr, kc):
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        r, c = kr+dr, kc+dc
        while 0 <= r < size and 0 <= c < size:
            if board[r][c] != '.':
                if board[r][c] in 'RQ': return True
                break
            r, c = r+dr, c+dc
    return False

def _check_diagonal(board, size, kr, kc):
    for dr, dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
        r, c = kr+dr, kc+dc
        while 0 <= r < size and 0 <= c < size:
            if board[r][c] != '.':
                if board[r][c] in 'BQ': return True
                break
            r, c = r+dr, c+dc
    return False

def _check_knight(board, size, kr, kc):
    for dr, dc in [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]:
        r, c = kr+dr, kc+dc
        if 0 <= r < size and 0 <= c < size and board[r][c] == 'N': return True
    return False

def _check_pawn(board, size, kr, kc):
    for dr, dc in [(-1,-1),(-1,1)]:
        r, c = kr+dr, kc+dc
        if 0 <= r < size and 0 <= c < size and board[r][c] == 'P': return True
    return False