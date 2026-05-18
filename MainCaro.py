from MiniMax_AlphaBeta import is_in, is_win, best_move, make_empty_board
import turtle

# Vẽ các button
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

    # Ghi chữ vào giữa nút (Căn chỉnh lại trục Y để chữ không bị lệch)
    t.goto((x1 + x2) / 2, (y1 + y2) / 2 + 0.3)
    t.color("#ffffff")
    t.write(text, align="center", font=("Arial", 13, "bold"))

# Vẽ menu
def draw_menu():

    global painter, size_board
    painter.clear()

    # Đổ nền cho Menu
    painter.goto(0, 0)
    painter.color("#2c3e50", "#f4f6f7")
    painter.begin_fill()
    painter.goto(size_board, 0)
    painter.goto(size_board, size_board)
    painter.goto(0, size_board)
    painter.end_fill()

    # Tiêu đề game
    painter.goto(size_board / 2, 2.5)
    painter.color("#2c3e50")
    painter.write("GAME CARO XO", align="center", font=("Arial", 26, "bold"))
    painter.goto(size_board / 2, 3.8)
    painter.write("Chọn chế độ chơi để bắt đầu", align="center", font=("Arial", 12, "italic"))

    # Vẽ các nút bấm menu
    draw_button(painter, 3, 5.5, 12, 7.0, "1. Người với Người", "#34495e")
    draw_button(painter, 3, 8.0, 12, 9.5, "2. Người với AI", "#16a085")
    draw_button(painter, 3, 10.5, 12, 12.0, "3. AI với AI", "#2980b9")

    screen.update()

# Khi chọn chế độ xong thì xóa menu và hiện bàn cờ
def start_game():

    global in_menu, painter, size_board, game_mode, screen
    in_menu = False
    painter.clear()

    bg_color = "#fafafa"
    # vẽ bàn cờ
    for r in range(size_board):
        for c in range(size_board):
            painter.goto(c, r + 1)
            draw_square(painter, 1, bg_color)
    screen.update()

    # Nếu chọn chế độ AI vs AI thì kích hoạt vòng lặp tự động của máy
    if game_mode == 3:
        screen.ontimer(ai_vs_ai_loop, 300)


def click(x, y):
    # khai báo các biến cục bộ để có thể đọc và ghi đè
    # kiểm tra nếu win thì sẽ dừng lại
    global board, colors, win, move_history, game_mode, turn, in_menu
    if win: return

    # nếu ở menu thì sẽ chọn chế độ chơi
    if in_menu:
        if 3 <= x <= 12:
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

   # nếu ở trong trận đấu
   # kiểm tra xem click có ra ngoài không
    ix, iy = int(x), int(y)
    if not is_in(board, iy, ix):
        return
    # nếu ô click còn trống thì xử lí tiếp còn không thì dừng
    if board[iy][ix] == ' ':
        # người với vời
        if game_mode == 1:
            draw_stone(ix, iy, turn)
            board[iy][ix] = turn
            move_history.append((ix, iy))

            status = is_win(board)
            if status != 'Continue playing':
                print(status)
                win = True
                return
            turn = 'w' if turn == 'b' else 'b'

        # người với ai
        elif game_mode == 2:
            draw_stone(ix, iy, 'b')
            board[iy][ix] = 'b'
            move_history.append((ix, iy))

            if is_win(board) != 'Continue playing':
                print(is_win(board))
                win = True
                return

            ay, ax = best_move(board, 'w')
            draw_stone(ax, ay, 'w')
            board[ay][ax] = 'w'
            move_history.append((ax, ay))

            if is_win(board) != 'Continue playing':
                print(is_win(board))
                win = True
                return


def ai_vs_ai_loop():

    global board, colors, win, move_history, turn, screen
    if win: return

    ay, ax = best_move(board, turn)
    draw_stone(ax, ay, turn)
    board[ay][ax] = turn
    move_history.append((ax, ay))

    status = is_win(board)
    if status != 'Continue playing':
        print(status)
        win = True
        return

    turn = 'w' if turn == 'b' else 'b'
    screen.ontimer(ai_vs_ai_loop, 600)

# vẽ 1 ô vuông
def draw_square(t, size, fill_color):
    t.color("#b2bec3", fill_color)
    t.pensize(1)
    t.pendown()
    for _ in range(4):
        t.forward(size)
        t.left(90)
    t.penup()


def initialize(size):
    global win, board, screen, colors, move_history, game_mode, turn, in_menu, painter, size_board

    size_board = size
    move_history = []
    win = False
    in_menu = True
    turn = 'b'  # 'b' sẽ đại diện cho X (đi trước), 'w' đại diện cho O
    board = make_empty_board(size)

    screen = turtle.Screen()
    screen.title("Caro")
    screen.setup(650, 650)
    screen.setworldcoordinates(0, size, size, 0)
    screen.tracer(0)

    painter = turtle.Turtle()
    painter.speed(0)
    painter.penup()
    painter.ht()

    # Tạo 2 bút vẽ riêng biệt cho X và O để nét vẽ mượt mà, không bị lẫn màu
    colors = {'b': turtle.Turtle(), 'w': turtle.Turtle()}

    # Thiết lập cho quân X (b) - Màu xanh lam Modern
    colors['b'].color('#2980b9')
    colors['b'].pensize(3)

    # Thiết lập cho quân O (w) - Màu đỏ cam Coral
    colors['w'].color('#e74c3c')
    colors['w'].pensize(3)

    for key in colors:
        colors[key].ht()
        colors[key].penup()
        colors[key].speed(0)

    # Hiển thị Menu đồ họa ngay khi mở ứng dụng
    draw_menu()

    screen.onclick(click)
    screen.listen()
    screen.mainloop()

# vẽ kí tự o x và căn giữ ô vuông
def draw_stone(x, y, player_turn):

    t = colors[player_turn]

    # Tâm thực tế của ô cờ
    center_x = x + 0.5
    center_y = y + 0.5

    if player_turn == 'b':
        # --- VẼ QUÂN X ---
        size = 0.25  # Độ nửa chiều rộng của chữ X

        # Nét chéo 1: Trên-Trái xuống Dưới-Phải
        t.penup()
        t.goto(center_x - size, center_y - size)
        t.pendown()
        t.goto(center_x + size, center_y + size)

        # Nét chéo 2: Dưới-Trái lên Trên-Phải
        t.penup()
        t.goto(center_x - size, center_y + size)
        t.pendown()
        t.goto(center_x + size, center_y - size)
        t.penup()

    else:
        # --- VẼ QUÂN O ---
        r = 0.25  # Bán kính đường tròn

        t.penup()
        # Trong hệ tọa độ đảo của bạn, để đường tròn tâm (center_x, center_y),
        # ta phải đưa rùa về vị trí đỉnh phía trên của đường tròn (center_y - r)
        t.goto(center_x, center_y - r)
        t.setheading(0)
        t.pendown()
        t.circle(r)
        t.penup()

    screen.update()


if __name__ == '__main__':
    initialize(15)