from MiniMax_AlphaBeta import is_in, is_win, best_move, make_empty_board
import turtle

def draw_button(t, x1, y1, x2, y2, text, fill_color):
    """Vẽ một nút bấm hình chữ nhật có văn bản ở giữa"""
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

    # Ghi chữ vào giữa nút
    t.goto((x1 + x2) / 2, (y1 + y2) / 2 + 0.2)
    t.color("#ffffff")
    t.write(text, align="center", font=("Arial", 13, "bold"))


def draw_menu():
    """Vẽ toàn bộ giao diện Menu chính lên màn hình"""
    global painter, size_board
    painter.clear()

    # Đổ nền cho Menu
    painter.goto(0, 0)
    painter.color("#2c3e50", "#eceff1")
    painter.begin_fill()
    painter.goto(size_board, 0)
    painter.goto(size_board, size_board)
    painter.goto(0, size_board)
    painter.end_fill()

    # Tiêu đề game
    painter.goto(size_board / 2, 2.5)
    painter.color("#2c3e50")
    painter.write("GAME CARO", align="center", font=("Arial", 24, "bold"))
    painter.goto(size_board / 2, 3.5)
    painter.write("Chọn chế độ chơi để bắt đầu", align="center", font=("Arial", 12, "italic"))

    # Vẽ 3 nút bấm tương ứng với 3 chế độ
    draw_button(painter, 3, 5.0, 12, 6.5, "1. Người vs Người (PvP)", "#34495e")
    draw_button(painter, 3, 7.5, 12, 9.0, "2. Người vs AI (PvAI)", "#16a085")
    draw_button(painter, 3, 10.0, 12, 11.5, "3. AI vs AI (Xem máy đấu)", "#2980b9")

    screen.update()


def start_game():
    """Xóa Menu và khởi tạo vẽ bàn cờ Caro"""
    global in_menu, painter, size_board, game_mode, screen
    in_menu = False
    painter.clear()

    bg_color = "#d7ccc8"  # Màu bàn cờ gỗ thanh lịch
    for r in range(size_board):
        for c in range(size_board):
            painter.goto(c, r + 1)
            draw_square(painter, 1, bg_color)
    screen.update()

    # Nếu chọn chế độ AI vs AI thì kích hoạt vòng lặp tự động của máy
    if game_mode == 3:
        screen.ontimer(ai_vs_ai_loop, 300)


def click(x, y):
    """Bộ xử lý trung tâm khi người dùng click chuột"""
    global board, colors, win, move_history, game_mode, turn, in_menu
    if win: return

    # --- NẾU ĐANG Ở MÀN HÌNH MENU ---
    if in_menu:
        if 3 <= x <= 12:
            if 5.0 <= y <= 6.5:
                game_mode = 1
                start_game()
            elif 7.5 <= y <= 9.0:
                game_mode = 2
                start_game()
            elif 10.0 <= y <= 11.5:
                game_mode = 3
                start_game()
        return

    # --- NẾU ĐANG TRONG TRẬN ĐẤU ---
    ix, iy = int(x), int(y)
    if not is_in(board, iy, ix):
        return

    if board[iy][ix] == ' ':
        # CHẾ ĐỘ 1: NGƯỜI VS NGƯỜI
        if game_mode == 1:
            draw_stone(ix, iy, colors[turn])
            board[iy][ix] = turn
            move_history.append((ix, iy))

            status = is_win(board)
            if status != 'Continue playing':
                print(status)
                win = True
                return
            turn = 'w' if turn == 'b' else 'b'

        # CHẾ ĐỘ 2: NGƯỜI VS AI
        elif game_mode == 2:
            draw_stone(ix, iy, colors['b'])
            board[iy][ix] = 'b'
            move_history.append((ix, iy))

            if is_win(board) != 'Continue playing':
                print(is_win(board))
                win = True
                return

            ay, ax = best_move(board, 'w')
            draw_stone(ax, ay, colors['w'])
            board[ay][ax] = 'w'
            move_history.append((ax, ay))

            if is_win(board) != 'Continue playing':
                print(is_win(board))
                win = True
                return


def ai_vs_ai_loop():
    """Vòng lặp tự động chạy dành riêng cho CHẾ ĐỘ 3: AI VS AI"""
    global board, colors, win, move_history, turn, screen
    if win: return

    ay, ax = best_move(board, turn)
    draw_stone(ax, ay, colors[turn])
    board[ay][ax] = turn
    move_history.append((ax, ay))

    status = is_win(board)
    if status != 'Continue playing':
        print(status)
        win = True
        return

    turn = 'w' if turn == 'b' else 'b'
    screen.ontimer(ai_vs_ai_loop, 600)  # Mỗi nước đi của AI cách nhau 600ms để người xem kịp theo dõi


def draw_square(t, size, fill_color):
    t.color("#2c3e50", fill_color)
    t.pendown()
    t.begin_fill()
    for _ in range(4):
        t.forward(size)
        t.left(90)
    t.end_fill()
    t.penup()


def initialize(size):
    global win, board, screen, colors, move_history, game_mode, turn, in_menu, painter, size_board

    size_board = size
    move_history = []
    win = False
    in_menu = True
    turn = 'b'
    board = make_empty_board(size)

    screen = turtle.Screen()
    screen.setup(650, 650)
    screen.setworldcoordinates(0, size, size, 0)
    screen.tracer(0)

    painter = turtle.Turtle()
    painter.speed(0)
    painter.penup()
    painter.ht()

    colors = {'w': turtle.Turtle(), 'b': turtle.Turtle()}
    colors['w'].color('#bdc3c7', '#ffffff')
    colors['b'].color('#1a1a1a', '#1a1a1a')

    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(0)

    # Hiển thị Menu đồ họa ngay khi mở ứng dụng
    draw_menu()

    screen.onclick(click)
    screen.listen()
    screen.mainloop()


def draw_stone(x, y, colturtle):
    r = 0.38
    colturtle.goto(x + 0.5, y + 0.5 - r)
    colturtle.setheading(0)
    colturtle.pendown()
    colturtle.begin_fill()
    colturtle.circle(r)
    colturtle.end_fill()
    colturtle.penup()
    screen.update()


if __name__ == '__main__':
    initialize(15)