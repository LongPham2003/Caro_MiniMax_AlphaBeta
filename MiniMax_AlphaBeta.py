
global move_history, game_mode, turn, in_menu, painter, size_board


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "] * sz)
    return board


def is_empty(board):
    for row in board:
        if any(cell != ' ' for cell in row):
            return False
    return True


def is_in(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board)


def is_win(board):
    black = score_of_col(board, 'b')
    white = score_of_col(board, 'w')
    sum_sumcol_values(black)
    sum_sumcol_values(white)
    if 5 in black and black[5] == 1:
        return 'Black won'
    elif 5 in white and white[5] == 1:
        return 'White won'
    if possible_moves(board) == []:
        return 'Draw'
    return 'Continue playing'



def march(board, y, x, dy, dx, length):
    curr_y, curr_x = y, x
    for _ in range(length):
        next_y = curr_y + dy
        next_x = curr_x + dx
        if is_in(board, next_y, next_x):
            curr_y, curr_x = next_y, next_x
        else:
            break
    return curr_y, curr_x


def score_ready(scorecol):
    sumcol = {0: {}, 1: {}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
    for key in scorecol:
        for score in scorecol[key]:
            if key in sumcol[score]:
                sumcol[score][key] += 1
            else:
                sumcol[score][key] = 1
    return sumcol


def sum_sumcol_values(sumcol):
    for key in sumcol:
        if key == 5:
            sumcol[5] = int(1 in sumcol[5].values())
        else:
            sumcol[key] = sum(sumcol[key].values())


def score_of_list(lis, col):
    blank = lis.count(' ')
    filled = lis.count(col)
    if blank + filled < 5:
        return -1
    elif blank == 5:
        return 0
    else:
        return filled


def row_to_list(board, y, x, dy, dx, yf, xf):
    row = []
    curr_y, curr_x = y, x
    while is_in(board, curr_y, curr_x):
        row.append(board[curr_y][curr_x])
        if curr_y == yf and curr_x == xf:
            break
        curr_y += dy
        curr_x += dx
    return row


def score_of_row(board, cordi, dy, dx, cordf, col):
    y, x = cordi
    yf, xf = cordf
    row = row_to_list(board, y, x, dy, dx, yf, xf)
    colscores = []
    for start in range(len(row) - 4):
        score = score_of_list(row[start:start + 5], col)
        colscores.append(score)
    return colscores


def score_of_col(board, col):
    f = len(board)
    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}
    for start in range(len(board)):
        scores[(0, 1)].extend(score_of_row(board, (start, 0), 0, 1, (start, f - 1), col))
        scores[(1, 0)].extend(score_of_row(board, (0, start), 1, 0, (f - 1, start), col))
        scores[(1, 1)].extend(score_of_row(board, (start, 0), 1, 1, (f - 1, f - 1 - start), col))
        scores[(-1, 1)].extend(score_of_row(board, (start, 0), -1, 1, (0, start), col))
        if start + 1 < len(board):
            scores[(1, 1)].extend(score_of_row(board, (0, start + 1), 1, 1, (f - 2 - start, f - 1), col))
            scores[(-1, 1)].extend(score_of_row(board, (f - 1, start + 1), -1, 1, (start + 1, f - 1), col))
    return score_ready(scores)


def score_of_col_one(board, col, y, x):
    scores = {(0, 1): [], (-1, 1): [], (1, 0): [], (1, 1): []}
    scores[(0, 1)].extend(score_of_row(board, march(board, y, x, 0, -1, 4), 0, 1, march(board, y, x, 0, 1, 4), col))
    scores[(1, 0)].extend(score_of_row(board, march(board, y, x, -1, 0, 4), 1, 0, march(board, y, x, 1, 0, 4), col))
    scores[(1, 1)].extend(score_of_row(board, march(board, y, x, -1, -1, 4), 1, 1, march(board, y, x, 1, 1, 4), col))
    scores[(-1, 1)].extend(score_of_row(board, march(board, y, x, -1, 1, 4), 1, -1, march(board, y, x, 1, -1, 4), col))
    return score_ready(scores)


def possible_moves(board):
    taken = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (-1, 1), (1, -1)]
    cord = {}
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] != ' ':
                taken.append((i, j))
    if not taken:
        return {(len(board) // 2, len(board) // 2): False}

    for direction in directions:
        dy, dx = direction
        for coord in taken:
            y, x = coord
            for length in [1, 2]:
                move = march(board, y, x, dy, dx, length)
                if board[move[0]][move[1]] == ' ' and move not in cord:
                    cord[move] = False
    return cord


def TF34score(score3, score4):
    for key4 in score4:
        if score4[key4] >= 1:
            for key3 in score3:
                if key3 != key4 and score3[key3] >= 2:
                    return True
    return False


def stupid_score(board, col, anticol, y, x):
    M = 1000
    res, adv, dis = 0, 0, 0
    board[y][x] = col
    sumcol = score_of_col_one(board, col, y, x)
    a = winning_situation(sumcol)
    adv += a * M
    sum_sumcol_values(sumcol)
    adv += sumcol[-1] + sumcol[1] + 4 * sumcol[2] + 8 * sumcol[3] + 16 * sumcol[4]

    board[y][x] = anticol
    sumanticol = score_of_col_one(board, anticol, y, x)
    d = winning_situation(sumanticol)
    dis += d * (M - 100)
    sum_sumcol_values(sumanticol)
    dis += sumanticol[-1] + sumanticol[1] + 4 * sumanticol[2] + 8 * sumanticol[3] + 16 * sumanticol[4]
    res = adv + dis
    board[y][x] = ' '
    return res


def winning_situation(sumcol):
    if 1 in sumcol[5].values():
        return 5
    elif len(sumcol[4]) >= 2 or (len(sumcol[4]) >= 1 and max(sumcol[4].values()) >= 2):
        return 4
    elif TF34score(sumcol[3], sumcol[4]):
        return 4
    else:
        score3 = sorted(sumcol[3].values(), reverse=True)
        if len(score3) >= 2 and score3[0] >= score3[1] >= 2: return 3
    return 0


def evaluate_board(board, col):
    anticol = 'b' if col == 'w' else 'w'
    total_score = 0
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == col:
                sumcol = score_of_col_one(board, col, y, x)
                sum_sumcol_values(sumcol)
                total_score += sumcol[-1] + sumcol[1] + 4 * sumcol[2] + 8 * sumcol[3] + 16 * sumcol[4]
            elif board[y][x] == anticol:
                sumanticol = score_of_col_one(board, anticol, y, x)
                sum_sumcol_values(sumanticol)
                total_score -= (
                        sumanticol[-1] + sumanticol[1] + 4 * sumanticol[2] + 8 * sumanticol[3] + 16 * sumanticol[4])
    return total_score


def minimax(board, depth, alpha, beta, is_maximizing, col):
    anticol = 'b' if col == 'w' else 'w'
    game_res = is_win(board)

    if depth == 0 or game_res != 'Continue playing':
        if game_res == 'White won': return (100000 + depth) if col == 'w' else (-100000 - depth)
        if game_res == 'Black won': return (-100000 - depth) if col == 'w' else (100000 + depth)
        if game_res == 'Draw': return 0
        return evaluate_board(board, col)

    all_moves = possible_moves(board)
    ranked_moves = []
    for move in all_moves:
        y, x = move
        score = stupid_score(board, col if is_maximizing else anticol, anticol if is_maximizing else col, y, x)
        ranked_moves.append((score, move))
    ranked_moves.sort(key=lambda x: x[0], reverse=True)
    best_moves = [move for score, move in ranked_moves[:4]]

    if is_maximizing:
        max_eval = -float('inf')
        for move in best_moves:
            y, x = move
            board[y][x] = col
            evaluation = minimax(board, depth - 1, alpha, beta, False, col)
            board[y][x] = ' '
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for move in best_moves:
            y, x = move
            board[y][x] = anticol
            evaluation = minimax(board, depth - 1, alpha, beta, True, col)
            board[y][x] = ' '
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval


def best_move(board, col):
    if is_empty(board):
        return (len(board) // 2, len(board) // 2)

    moves = possible_moves(board)
    best_val = -float('inf')
    movecol = None

    anticol = 'b' if col == 'w' else 'w'
    ranked_moves = []
    for move in moves:
        y, x = move
        score = stupid_score(board, col, anticol, y, x)
        ranked_moves.append((score, move))
    ranked_moves.sort(key=lambda x: x[0], reverse=True)

    top_candidates = ranked_moves[:6]
    depth = 2

    for score, move in top_candidates:
        y, x = move
        board[y][x] = col
        move_val = minimax(board, depth - 1, -float('inf'), float('inf'), False, col)
        board[y][x] = ' '

        if move_val > best_val:
            best_val = move_val
            movecol = move

    return movecol
