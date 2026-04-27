def checkmate(board_data):
    
    if isinstance(board_data, str):
        board = board_data.strip().split('\n')
    else:
        board = board_data

    size = len(board)
    king_pos = None

    for r in range(size):
        for c in range(size):
            if board[r][c] == 'K':
                king_pos = (r, c)
                break
        if king_pos: break
    
    if not king_pos: return

    kr, kc = king_pos
    straight = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    diagonal = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dr, dc in straight:
        r, c = kr + dr, kc + dc
        while 0 <= r < size and 0 <= c < size:
            if board[r][c] != '.':
                if board[r][c] in ('R', 'Q'):
                    print("Success")
                    return
                break
            r, c = r + dr, c + dc

    for dr, dc in diagonal:
        r, c = kr + dr, kc + dc
        while 0 <= r < size and 0 <= c < size:
            if board[r][c] != '.':
                if board[r][c] in ('B', 'Q'):
                    print("Success")
                    return
                break
            r, c = r + dr, c + dc

    for dr, dc in [(1, -1), (1, 1)]:
        r, c = kr + dr, kc + dc
        if 0 <= r < size and 0 <= c < size:
            if board[r][c] == 'P':
                print("Success")
                return

    print("Fail")