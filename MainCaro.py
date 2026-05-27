import turtle
from MiniMax_AlphaBeta import is_in, check_winner, get_best_move, make_empty_board

ai_timer_id = None


# Vẽ một nút bấm hình chữ nhật có chữ ở giữa
def draw_button(t, x1, y1, x2, y2, text, fill_color):

    t.penup()
    t.goto(x1, y1)
    t.color("#2c3e50", fill_color)
    t.pendown()
    t.begin_fill()
    t.goto(x2, y1)
    t.goto(x2, y2)
    t.goto(x1, y2)
    t.goto(x1, y1)
    t.end_fill()
    t.penup()

    # Căn chữ vào giữa nút bấm
    t.goto((x1 + x2) / 2, (y1 + y2) / 2 + 0.3)
    t.color("#ffffff")
    t.write(text, align="center", font=("Arial", 13, "bold"))


def draw_menu():
    global painter, size_board
    painter.clear()

    # Tạo màu nền Menu
    painter.goto(0, 0)
    painter.color("#2c3e50", "#f4f6f7")
    painter.begin_fill()
    painter.goto(size_board, 0)
    painter.goto(size_board, size_board + 1.5)
    painter.goto(0, size_board + 1.5)
    painter.end_fill()

    # Viết tiêu đề game
    painter.goto(size_board / 2, size_board * 0.15)
    painter.color("#2c3e50")
    painter.write("GAME CARO XO", align="center", font=("Arial", 28, "bold"))

    painter.goto(size_board / 2, size_board * 0.25)
    painter.write("Chọn chế độ chơi để bắt đầu", align="center", font=("Arial", 12, "italic"))

    # Tính toán tọa độ đặt nút bấm căn theo kích thước bàn cờ
    mid = size_board / 2
    draw_button(painter, mid - 4.5, 5.5, mid + 4.5, 7.0, "1. Người với Người", "#34495e")
    draw_button(painter, mid - 4.5, 8.0, mid + 4.5, 9.5, "2. Người với AI", "#16a085")
    draw_button(painter, mid - 4.5, 10.5, mid + 4.5, 12.0, "3. AI với AI", "#2980b9")

    screen.update()


def draw_turn_indicator():
    # Hàm vẽ thông báo lượt đi hiện tại của X hoặc O
    global painter, size_board, turn, win

    if win: return

    # Xóa vùng hiển thị lượt đi cũ
    painter.penup()
    painter.goto(0.5, size_board + 0.2)
    painter.color("#fafafa", "#fafafa")
    painter.pendown()
    painter.begin_fill()
    painter.goto(4.5, size_board + 0.2)
    painter.goto(4.5, size_board + 1.2)
    painter.goto(0.5, size_board + 1.2)
    painter.goto(0.5, size_board + 0.2)
    painter.end_fill()
    painter.penup()

    # Ghi chữ hiển thị lượt
    painter.goto(0.5, size_board + 0.9)
    painter.color("#2c3e50")
    painter.write("Lượt đi:", align="left", font=("Arial", 12, "bold"))

    # Vẽ ký hiệu X hoặc O nhỏ ngay bên cạnh chữ
    center_x = 3.0
    center_y = size_board + 0.65

    if turn == 'b':
        painter.color('#2980b9')
        painter.pensize(3)
        size = 0.15
        painter.goto(center_x - size, center_y - size)
        painter.pendown()
        painter.goto(center_x + size, center_y + size)
        painter.penup()
        painter.goto(center_x - size, center_y + size)
        painter.pendown()
        painter.goto(center_x + size, center_y - size)
        painter.penup()
    else:
        painter.color('#e74c3c')
        painter.pensize(3)
        r = 0.15
        painter.goto(center_x, center_y - r)
        painter.setheading(0)
        painter.pendown()
        painter.circle(r)
        painter.penup()

# Hàm phụ trách reset toàn bộ dữ liệu bàn cờ về trạng thái ban đầu
def reset_board_state():

    global win, board, turn, move_history, colors, size_board
    win = False
    turn = 'b'
    move_history = []
    board = make_empty_board(size_board)
    colors['b'].clear()
    colors['w'].clear()

# Hủy trận đấu hiện tại và quay về màn hình chính
def back_to_menu():

    global in_menu
    in_menu = True
    reset_board_state()
    draw_menu()


def start_game():
    global in_menu, painter, size_board, game_mode, screen
    in_menu = False
    painter.clear()

    bg_color = "#fafafa"
    # Vẽ các ô vuông của bàn cờ
    for r in range(size_board):
        for c in range(size_board):
            painter.goto(c, r)
            draw_square(painter, 1, bg_color)

    # Vẽ nút Quay về Menu
    draw_button(painter, size_board - 5.5, size_board + 0.2, size_board - 0.5, size_board + 1.2, "⬅ Menu", "#e74c3c")

    # Vẽ hiển thị lượt đi đầu tiên
    draw_turn_indicator()

    screen.update()

    if game_mode == 3:
        global ai_timer_id
        ai_timer_id = screen.ontimer(ai_vs_ai_loop, 300)


def display_end_game(status_text):
    global painter, size_board
    mid = size_board / 2

    # Xóa khu vực hiển thị lượt đi dưới đáy vì game đã kết thúc
    painter.penup()
    painter.goto(0.5, size_board + 0.2)
    painter.color("#fafafa", "#fafafa")
    painter.pendown()
    painter.begin_fill()
    painter.goto(4.5, size_board + 0.2)
    painter.goto(4.5, size_board + 1.2)
    painter.goto(0.5, size_board + 1.2)
    painter.goto(0.5, size_board + 1.2)
    painter.end_fill()
    painter.penup()


    draw_button(painter, mid - 4.5, mid - 2.2, mid + 4.5, mid - 0.9, status_text, "#f39c12")

    draw_button(painter, mid - 4.5, mid - 0.5, mid + 4.5, mid + 0.8, "Chơi Tiếp 🔄", "#27ae60")

    draw_button(painter, mid - 4.5, mid + 1.2, mid + 4.5, mid + 2.5, "Thoát Game ❌", "#e74c3c")

    screen.update()


def click(x, y):
    global board, win, move_history, game_mode, turn, in_menu, screen

    # Xử lý click chọn chế độ ở Menu
    if in_menu:
        mid = size_board / 2
        if mid - 4.5 <= x <= mid + 4.5:
            if 5.5 <= y <= 7.0:
                game_mode = 1
                start_game()
            elif 8.0 <= y <= 9.5:
                game_mode = 2
                start_game()
            elif 10.5 <= y <= 12.0:
                game_mode = 3
                start_game()
        return

    # Kiểm tra bấm nút quay về Menu nhỏ (ở góc dưới bên phải đáy bàn cờ lúc đang chơi)
    if (size_board - 5.5 <= x <= size_board - 0.5) and (size_board + 0.2 <= y <= size_board + 1.2):
        if not win:
            back_to_menu()
            return

    # Kiểm tra click khi kết thúc trận đấu
    if win:
        mid = size_board / 2

        # Click nút "Chơi Tiếp"
        if (mid - 4.5 <= x <= mid + 4.5) and (mid - 0.5 <= y <= mid + 0.8):
            reset_board_state()
            start_game()
            return

        # Click nút "Thoát Game"
        elif (mid - 4.5 <= x <= mid + 4.5) and (mid + 1.2 <= y <= mid + 2.5):
            # Đóng cửa sổ ứng dụng Turtle ngay lập tức
            screen.bye()
            return

        return

    # Lấy vị trí quân cờ vừa mới đánh (0,1,2...)
    ix, iy = int(x), int(y)

    # Kiểm tra tọa độ vừa click có nằm trong phạm vi 15x15 không
    if not is_in(board, iy, ix):
        # click trượt thì không làm gì cả
        return

    # Kiểm tra xem vị trí còn trống hay không
    # x là trục ngang (dòng) y là trục dọc (cột)
    if board[iy][ix] == ' ':
        # nếu chế độ người vs người
        if game_mode == 1:
            # gọi hàm vẽ quân cờ lên màn hình tại (x,y)
            draw_stone(ix, iy, turn)
             # lưu trạng thái xem quân vừa đi là x hay o
            board[iy][ix] = turn
            move_history.append((iy, ix))
            # kiểm tra xem nước vừa đi đã thắng chưa
            status = check_winner(board)
            # nếu thắng dừng và thông báo
            if status != 'Continue':
                win = True
                display_end_game("HÒA CỜ!" if status == "Draw" else f"QUÂN {status.upper()} THẮNG!")
                return

            # Đổi lượt đi nếu hiện tại là 'b' (Đen/X) thì lượt sau là 'w' (Trắng/O)
            turn = 'w' if turn == 'b' else 'b'
            # Cập nhật lại biểu tượng hiển thị lượt đi dưới màn hình
            draw_turn_indicator()

        elif game_mode == 2:
            # Lượt của người mặc định x (X - 'b')
            draw_stone(ix, iy, 'b')
            board[iy][ix] = 'b'
            move_history.append((iy, ix))

            status = check_winner(board)
            if status != 'Continue':
                win = True
                display_end_game("HÒA CỜ!" if status == "Draw" else "BẠN ĐÃ THẮNG!")
                return

            turn = 'w'
            draw_turn_indicator()
            screen.update()

            if in_menu: return

            # Lượt của AI (O - 'w')
            # Gọi thuật toán MiniMax Alpha-Beta để tìm nước đi (dòng ay, cột ax) tốt nhất cho quân 'w'
            ay, ax = get_best_move(board, 'w')
            # Kiểm tra lại một lần nữa xem người chơi có thoát game khi AI đang tính toán không
            if in_menu: return
            # vẽ quân của ai lên màn hình
            draw_stone(ax, ay, 'w')
            #  cập nhật vào ma trận
            board[ay][ax] = 'w'
            move_history.append((ay, ax))

            status = check_winner(board)
            if status != 'Continue':
                win = True
                display_end_game("HÒA CỜ!" if status == "Draw" else "AI ĐÃ THẮNG!")
                return

            turn = 'b'
            draw_turn_indicator()


# ai vs ai
def ai_vs_ai_loop():
    global board, win, move_history, turn, screen, in_menu
    if win or in_menu: return

    ay, ax = get_best_move(board, turn)
    if in_menu: return

    draw_stone(ax, ay, turn)
    board[ay][ax] = turn
    move_history.append((ay, ax))

    status = check_winner(board)
    if status != 'Continue':
        win = True
        display_end_game("HÒA CỜ!" if status == "Draw" else f"AI {turn.upper()} THẮNG!")
        return

    turn = 'w' if turn == 'b' else 'b'
    draw_turn_indicator()

    # yêu cầu gọi lại hàm để ai đánh với ai
    screen.ontimer(ai_vs_ai_loop, 600)


def draw_square(t, size, fill_color):
    t.color("#b2bec3", fill_color)
    t.pensize(1)
    t.pendown()
    # Vòng lặp vẽ 4 cạnh ô vuông
    for _ in range(4):
        # Tiến tới 1 đơn vị
        t.forward(size)
        # Quay trái 90 độ
        t.left(90)
    t.penup()

# hàm vẽ ký hiệu quân cờ hình X hoặc O vào chính giữa ô vuông có tọa độ (x, y)
def draw_stone(x, y, player_turn):
    t = colors[player_turn]        # Lấy ra con rùa tương ứng: rùa của 'b' vẽ màu xanh, rùa của 'w' vẽ màu đỏ
    center_x = x + 0.5             # Tính toán tọa độ tâm X của ô (cộng thêm 0.5 để vào giữa ô kích thước 1x1)
    center_y = y + 0.5             # Tính toán tọa độ tâm Y của ô

    if player_turn == 'b':
        # Vẽ quân x
        size = 0.25                # Độ rộng của nét gạch X
        # Nét gạch thứ nhất: Từ góc dưới-trái lên trên-phải
        t.penup()
        t.goto(center_x - size, center_y - size)
        t.pendown()
        t.goto(center_x + size, center_y + size)
        # Nét gạch thứ hai: Từ góc trên-trái xuống dưới-phải
        t.penup()
        t.goto(center_x - size, center_y + size)
        t.pendown()
        t.goto(center_x + size, center_y - size)
        t.penup()
    else:
        # Vẽ quân o
        r = 0.25                   # Bán kính hình tròn
        t.penup()
        t.goto(center_x, center_y - r) # Di chuyển rùa tới điểm đáy của đường tròn để khi vẽ tâm sẽ nằm chuẩn giữa ô
        t.setheading(0)            # Đặt hướng rùa nhìn sang bên phải
        t.pendown()
        t.circle(r)                # Lệnh vẽ hình tròn bán kính r
        t.penup()

    screen.update()


def initialize(size):
    global win, board, screen, colors, move_history, game_mode, turn, in_menu, painter, size_board

    size_board = size
    move_history = []
    win = False
    in_menu = True
    turn = 'b'  # Quân 'b' (X) luôn mặc định đi trước
    board = make_empty_board(size)  # Tạo một ma trận 2 chiều rỗng cỡ 15x15 chứa toàn ký tự trống ' '

    screen = turtle.Screen()
    screen.title("Gomoku Caro AI - Phiên bản Mới")
    screen.setup(650, 700)  # Thiết lập kích thước cửa sổ: Rộng 650 pixel, Cao 700 pixel

    # Lệnh này định nghĩa: Góc TRÊN - TRÁI màn hình là gốc (0, 0)
    # Góc DƯỚI - PHẢI màn hình có tọa độ là (size, size + 1.5) tức là (15, 16.5)
    # Việc cộng thêm 1.5 đơn vị ở trục Y để chừa ra một khoảng trống dài dưới đáy bàn cờ làm chỗ vẽ nút bấm và hiển thị lượt đi.
    screen.setworldcoordinates(0, size + 1.5, size, 0)

    screen.tracer(
        0)  # Tắt chế độ tự động vẽ hoạt ảnh của rùa (giúp bàn cờ và quân cờ hiện ra lập tức, không bị giật lag)

    # Khởi tạo con rùa 'painter' chuyên làm nhiệm vụ vẽ khung bàn cờ, menu và các nút bấm
    painter = turtle.Turtle()
    painter.speed(0)
    painter.penup()
    painter.ht()  # Ẩn hình tam giác của con rùa đi (ht = hide turtle)

    # Khởi tạo 2 con rùa riêng biệt quản lý vẽ quân cờ nhằm tối ưu bộ nhớ
    colors = {'b': turtle.Turtle(), 'w': turtle.Turtle()}
    colors['b'].color('#2980b9')  # Thiết lập màu xanh dương cho quân X
    colors['b'].pensize(3)  # Độ dày nét vẽ chữ X là 3 pixel
    colors['w'].color('#e74c3c')  # Thiết lập màu đỏ cho quân O
    colors['w'].pensize(3)  # Độ dày nét vẽ hình tròn O là 3 pixel

    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(0)

    draw_menu()  # Gọi hàm vẽ Menu chính lên đầu tiên khi vừa bật game

    screen.onclick(click)  # Đăng ký sự kiện: Mỗi khi chuột click vào bất kỳ đâu trên màn hình, Python sẽ tự động gọi hàm click(x, y)
    screen.listen()  # Ra lệnh cho cửa sổ tập trung lắng nghe các sự kiện chuột/bàn phím
    screen.mainloop()  # Vòng lặp vô tận giữ cho cửa sổ game luôn mở không bị tắt đi


if __name__ == '__main__':
    initialize(15)