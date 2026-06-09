import time

# Khai báo một biến toàn cục để đếm số nút đã duyệt
node_count = 0
#  tạo bàn cờ sz x sz
def make_empty_board(sz):
    return [[" "] * sz for _ in range(sz)]

# kiểm tra tọa độ x hàng y cột
def is_in(board, y, x):
    return 0 <= y < len(board) and 0 <= x < len(board)


def evaluate_line_fixed(board, y, x, dy, dx, player):
    #Từ ô (y,x), đi về phía trước và phía sau theo hướng (dy,dx) để đếm quân
    count_player = 1  # quân mình
    open_ends = 0   # xem ô còn  trống ko

    # 1. quét tiền về phía trước nếu gặp quân mình ...
    i = 1
    while is_in(board, y + i * dy, x + i * dx) and board[y + i * dy][x + i * dx] == player:
        count_player += 1
        i += 1
    # quét đầu phía trước có trống không ...
    if is_in(board, y + i * dy, x + i * dx) and board[y + i * dy][x + i * dx] == ' ':
        open_ends += 1

    # 2. Lùi về phía sau ...
    i = 1
    while is_in(board, y - i * dy, x - i * dx) and board[y - i * dy][x - i * dx] == player:
        count_player += 1
        i += 1
    # quét phía sau có trống không ...
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
    # Nếu AI đang giữ quân Đen ('b'), đối thủ sẽ là quân Trắng ('w') và ngược lại
    opponent = 'w' if player == 'b' else 'b'
    directions = [
        (0, 1),  # trục ngang (Không đổi dòng, tăng cột)
        (1, 0),  # trục dọc (Tăng dòng, không đổi cột)
        (1, 1),  # Đường Chéo Xuôi (Chạy từ trên-trái xuống dưới-phải)
        (-1, 1)  # Đường Chéo Ngược (Chạy từ dưới-trái lên trên-phải)
    ]

    board[y][x] = player  # Đánh thử để tính điểm

    total_attack = 0
    total_defense = 0

    for dy, dx in directions:
        # Tính xem nếu ta đánh vào đây thì hướng này được bao nhiêu điểm
        total_attack += evaluate_line_fixed(board, y, x, dy, dx, player)
        # Tính xem nếu ĐỊCH đánh vào đây thì hướng này mạnh thế nào (để ta đi chặn)
        total_defense += evaluate_line_fixed(board, y, x, dy, dx, opponent)

    board[y][x] = ' '  # Trả lại ô trống

    # Cộng điểm Tấn công + Phòng thủ (nhân hệ số chặn địch cao hơn một chút để AI thông minh hơn)
    return total_attack + int(total_defense * 1.3)

#  TÌM CÁC NƯỚC ĐI TIỀM NĂNG (Xung quanh các quân đã đánh trong bán kính 2 ô)
def get_possible_moves(board):
    size = len(board)
    moves = set()
    has_pieces = False # xem bàn cờ đã có quân nào chưa

    for y in range(size): # duyệt qua toàn bộ bàn cờ ô nào 0 trống thì sẽ là true và sẽ phủ sóng
        for x in range(size): # xung quanh quân cờ này
            if board[y][x] != ' ':
                has_pieces = True
                # Lấy các ô trống xung quanh ô đã đánh
                # quét ma trận 5x5 xung quanh với quân cờ nằm ở chính giữa
                # nếu ny nx hàng xóm mà nằm trong bàn cờ và còn ' ' thì thêm vào ds tiềm năng
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
                    # Kiểm tra xem có đủ 5 quân liên tiếp  không
                    if all(is_in(board, y + i * dy, x + i * dx) and board[y + i * dy][x + i * dx] == player for i in
                           range(5)):
                        return f"{player} won"

    if not get_possible_moves(board):
        return "Draw"
    return "Continue"


# 7. THUẬT TOÁN MINIMAX KẾT HỢP CẮT TỈA ALPHA-BETA
def minimax(board, depth, alpha, beta, is_maximizing, player):
    global node_count
    node_count += 1  # 2. Mỗi lần hàm minimax được gọi, tăng số nút lên 1

    winner = check_winner(board)
    if winner != "Continue" or depth == 0:
        if winner == f"{player} won":
            return 100000 + depth
        elif "won" in winner:
            return -100000 - depth
        elif winner == "Draw":
            return 0
        return 0

    opponent = "w" if player == "b" else "b"
    current_player = player if is_maximizing else opponent

    moves = get_possible_moves(board)
    moves.sort(
        key=lambda m: evaluate_move(board, m[0], m[1], current_player),
        reverse=True,
    )
    # AI chỉ giữ lại 4 nước đi tốt nhất để tính toán sâu xuống tiếp.
    best_moves = moves[:4]

    if is_maximizing:
        max_eval = -float("inf")  # Khởi tạo điểm cực đại ban đầu là âm vô cùng
        for y, x in best_moves:
            board[y][x] = player  # Đánh thử quân của Ta
            evaluation = minimax(board, depth - 1, alpha, beta, False,
                                 player)  # Gọi đệ quy, lượt sau là của Địch (False)
            board[y][x] = " "  # Thu quân về (Hoàn tác)
            max_eval = max(max_eval, evaluation)  # Cập nhật điểm cao nhất có thể đạt được
            alpha = max(alpha, evaluation)  # Cập nhật ranh giới Alpha
            if beta <= alpha:
                break  # Cắt tỉa Alpha-Beta
        return max_eval
    else:
        min_eval = float("inf")  # Khởi tạo điểm cực tiểu ban đầu là dương vô cùng
        for y, x in best_moves:
            board[y][x] = opponent  # Đánh thử quân của Địch
            evaluation = minimax(board, depth - 1, alpha, beta, True, player)  # Gọi đệ quy, lượt sau là của Ta (True)
            board[y][x] = " "  # Thu quân về (Hoàn tác)
            min_eval = min(min_eval, evaluation)  # Đối thủ sẽ chọn nước làm điểm của Ta thấp nhất
            beta = min(beta, evaluation)  # Cập nhật ranh giới Beta
            if beta <= alpha:
                break  # Cắt tỉa Alpha-Beta
        return min_eval


def get_best_move(board, player):
    global node_count
    node_count = 0  # Reset lại số nút về 0 trước khi AI tính nước mới

    moves = get_possible_moves(board)
    if len(moves) == 1:
        return moves[0]

    # 3. Ghi lại thời điểm bắt đầu tính toán
    start_time = time.time()

    best_val = -float("inf")
    best_move = None

    moves.sort(
        key=lambda m: evaluate_move(board, m[0], m[1], player), reverse=True
    )
    candidates = moves[:6]

    for y, x in candidates:
        board[y][x] = player
        move_val = minimax(
            board, 4, -float("inf"), float("inf"), False, player
        )  # Độ sâu depth = 4
        board[y][x] = " "

        if move_val > best_val:
            best_val = move_val
            best_move = (y, x)

    # 4. Ghi lại thời điểm kết thúc và tính toán hiệu năng
    end_time = time.time()
    execution_time = end_time - start_time

    # 5. In kết quả ra màn hình PyCharm để lấy số liệu làm báo cáo
    print("\n--- THÔNG SỐ KIỂM THỬ HIỆU NĂNG AI ---")
    print(f"Nước đi được chọn: {best_move}")
    print(f"Tổng số nút (trạng thái) đã duyệt: {node_count} nút")
    print(f"Thời gian phản hồi của AI: {execution_time:.4f} giây")
    print("---------------------------------------\n")

    return best_move