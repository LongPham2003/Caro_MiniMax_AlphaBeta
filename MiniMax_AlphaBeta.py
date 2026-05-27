
#  tạo bàn cờ sz x sz
def make_empty_board(sz):
    return [[" "] * sz for _ in range(sz)]

# kiểm tra tọa độ
def is_in(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board)


def evaluate_line_fixed(board, y, x, dy, dx, player):
    #Từ ô (y,x), đi về phía trước và phía sau theo hướng (dy,dx) để đếm quân
    count_player = 1
    open_ends = 0

    # 1. Tiến về phía trước
    i = 1
    while is_in(board, y + i * dy, x + i * dx) and board[y + i * dy][x + i * dx] == player:
        count_player += 1
        i += 1
    # Kiểm tra đầu phía trước có trống không
    if is_in(board, y + i * dy, x + i * dx) and board[y + i * dy][x + i * dx] == ' ':
        open_ends += 1

    # 2. Lùi về phía sau
    i = 1
    while is_in(board, y - i * dy, x - i * dx) and board[y - i * dy][x - i * dx] == player:
        count_player += 1
        i += 1
    # Kiểm tra đầu phía sau có trống không
    if is_in(board, y - i * dy, x - i * dx) and board[y - i * dy][x - i * dx] == ' ':
        open_ends += 1

    # Trả về điểm số dựa trên độ mạnh của chuỗi theo hướng này
    if count_player >= 5: return 1000000  # Thắng luôn
    if count_player == 4:
        return 50000 if open_ends > 0 else 5000  # 4 quân thoáng đầu vs bị chặn 1 đầu
    if count_player == 3:
        return 8000 if open_ends == 2 else 800  # 3 quân thoáng 2 đầu cực nguy hiểm
    if count_player == 2:
        return 500 if open_ends == 2 else 50
    return 10


def evaluate_move(board, y, x, player):
    # Hàm chấm điểm
    opponent = 'w' if player == 'b' else 'b'
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    board[y][x] = player  # Đánh thử

    total_attack = 0
    total_defense = 0

    for dy, dx in directions:
        # Tính xem nếu ta đánh vào đây thì hướng này được bao nhiêu điểm
        total_attack += evaluate_line_fixed(board, y, x, dy, dx, player)
        # Tính xem nếu ĐỊCH đánh vào đây thì hướng này mạnh thế nào (để ta đi chặn)
        total_defense += evaluate_line_fixed(board, y, x, dy, dx, opponent)

    board[y][x] = ' '  # Trả lại ô trống

    # Cộng điểm Tấn công + Phòng thủ (nhân hệ số chặn địch cao hơn một chút để AI khôn hơn)
    return total_attack + int(total_defense * 1.3)
# 5. TÌM CÁC NƯỚC ĐI TIỀM NĂNG (Xung quanh các quân đã đánh trong bán kính 2 ô)
def get_possible_moves(board):
    size = len(board)
    moves = set()
    has_pieces = False

    for y in range(size):
        for x in range(size):
            if board[y][x] != ' ':
                has_pieces = True
                # Lấy các ô trống xung quanh ô đã đánh
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        ny, nx = y + dy, x + dx
                        if is_in(board, ny, nx) and board[ny][nx] == ' ':
                            moves.add((ny, nx))

    # Nếu bàn cờ trống, chọn ngay ô chính giữa
    if not has_pieces:
        return [(size // 2, size // 2)]

    return list(moves)


# 6. KIỂM TRA XEM AI THẮNG
def check_winner(board):
    size = len(board)
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for y in range(size):
        for x in range(size):
            if board[y][x] != ' ':
                player = board[y][x]
                for dy, dx in directions:
                    # Kiểm tra xem có đủ 5 quân liên tiếp cùng màu không
                    if all(is_in(board, y + i * dy, x + i * dx) and board[y + i * dy][x + i * dx] == player for i in
                           range(5)):
                        return f"{player} won"

    if not get_possible_moves(board):
        return "Draw"
    return "Continue"


# 7. THUẬT TOÁN MINIMAX KẾT HỢP CẮT TỈA ALPHA-BETA
def minimax(board, depth, alpha, beta, is_maximizing, player):
    winner = check_winner(board)
    if winner != "Continue" or depth == 0:
        if winner == f"{player} won":
            return 100000 + depth
        elif "won" in winner:
            return -100000 - depth  # Đối thủ thắng
        elif winner == "Draw":
            return 0
        return 0

    opponent = 'w' if player == 'b' else 'b'
    current_player = player if is_maximizing else opponent

    moves = get_possible_moves(board)
    # Sắp xếp các nước đi có điểm cao lên trước để cắt tỉa Alpha-Beta hiệu quả hơn
    moves.sort(key=lambda m: evaluate_move(board, m[0], m[1], current_player), reverse=True)

    # Giới hạn chỉ duyệt 4 nước đi tốt nhất để không bị chậm máy
    best_moves = moves[:4]

    if is_maximizing:
        max_eval = -float('inf')
        for y, x in best_moves:
            board[y][x] = player
            evaluation = minimax(board, depth - 1, alpha, beta, False, player)
            board[y][x] = ' '
            max_eval = max(max_eval, evaluation)
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = float('inf')
        for y, x in best_moves:
            board[y][x] = opponent
            evaluation = minimax(board, depth - 1, alpha, beta, True, player)
            board[y][x] = ' '
            min_eval = min(min_eval, evaluation)
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return min_eval


def get_best_move(board, player):
    moves = get_possible_moves(board)
    if len(moves) == 1:  # Nước đi đầu tiên vào giữa bàn cờ
        return moves[0]

    best_val = -float('inf')
    best_move = None

    # Lấy ra 6 nước đi tốt nhất dựa trên chấm điểm nhanh để đưa vào Minimax sâu hơn
    moves.sort(key=lambda m: evaluate_move(board, m[0], m[1], player), reverse=True)
    candidates = moves[:6]

    for y, x in candidates:
        board[y][x] = player
        # Gọi Minimax với độ sâu là 4 lượt đi tiếp theo
        move_val = minimax(board, 4, -float('inf'), float('inf'), False, player)
        board[y][x] = ' '

        if move_val > best_val:
            best_val = move_val
            best_move = (y, x)

    return best_move