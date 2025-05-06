from pyray import *
import random
from chess_board import get_texture

# Screen and UI constants
SCREEN_W = 1920
SCREEN_H = 1080
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 70
BUTTON_SPACING = 40
BUTTON_X = SCREEN_W - BUTTON_WIDTH - 60  # Sidebar
BUTTON_Y = 800  # Fixed position for switch turn button

# Timer settings
STARTING_TIME = 600.0  # 10 minutes in seconds
white_time = STARTING_TIME
black_time = STARTING_TIME
active_timer = None  # "white" or "black"
last_timer_update = 0.0

# Promotion settings
promotion_choices = ["Queen", "Rook", "Bishop", "Knight"]
PROMOTION_WIDTH = 500
PROMOTION_HEIGHT = 300

# UI Rects
toggle_btn = Rectangle(BUTTON_X, BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT)


def draw_promotion_popup(board):
    if board.promotion is not None:
        mouse_pos = get_mouse_position()
        mouse_clicked = is_mouse_button_pressed(MOUSE_LEFT_BUTTON)

        promotion_rect = Rectangle(
            (get_screen_width() - PROMOTION_WIDTH) // 2,
            (get_render_height() - PROMOTION_HEIGHT) // 2,
            PROMOTION_WIDTH,
            PROMOTION_HEIGHT
        )

        draw_rectangle(0, 0, get_screen_width(),
                       get_screen_height(), Color(0, 0, 0, 100))
        draw_rectangle_rec(promotion_rect, Color(245, 245, 245, 240))
        draw_rectangle_lines_ex(promotion_rect, 4, DARKGRAY)
        draw_text("Promote to:", int(promotion_rect.x + 20),
                  int(promotion_rect.y + 20), 24, BLACK)

        for i, name in enumerate(promotion_choices):
            btn_rect = Rectangle(promotion_rect.x + 30 +
                                 i * 90, promotion_rect.y + 80, 80, 40)
            hovered = check_collision_point_rec(mouse_pos, btn_rect)
            draw_rectangle_rec(btn_rect, DARKGRAY if hovered else LIGHTGRAY)
            draw_text(name, int(btn_rect.x + 10),
                      int(btn_rect.y + 10), 16, BLACK)

            if hovered and mouse_clicked:
                board.promote_to = name.lower()


def listen_timer(board):
    current_turn = "white" if board.player1.is_turn else "black"

    if last_timer_update == 0 and board.player2.is_turn:
        toggle_timer()

    if is_key_pressed(KeyboardKey.KEY_SPACE):
        if active_timer != current_turn:
            toggle_timer()


def update_timers():
    global white_time, black_time, last_timer_update

    if active_timer is None:
        return

    now = get_time()
    delta = now - last_timer_update
    last_timer_update = now

    if active_timer == "white":
        white_time = max(0.0, white_time - delta)
    elif active_timer == "black":
        black_time = max(0.0, black_time - delta)


def draw_timers():
    def format_time(t):
        minutes = int(t // 60)
        seconds = int(t % 60)
        return f"{minutes:02}:{seconds:02}"

    draw_text(format_time(white_time), 1220, 365, 90, BLACK)
    draw_text(format_time(black_time), 1525, 365, 90, BLACK)


def toggle_timer():
    global active_timer, last_timer_update
    active_timer = "white" if active_timer == "black" else "black"
    last_timer_update = get_time()


def draw_timer_texture():
    draw_texture(get_texture("timer"), 1110, 200, WHITE)
    tex = get_texture("timer_button")

    if active_timer == "white":
        draw_texture(tex, 1231, 180, WHITE)
    else:
        draw_texture_pro(
            tex,
            # source rectangle (flipped)
            Rectangle(0, 0, -tex.width, tex.height),
            Rectangle(1231, 180, tex.width, tex.height),  # destination
            Vector2(0, 0),
            0,
            WHITE
        )


def draw_buttons(board):
    global last_timer_update
    global white_time
    global black_time
    global active_timer
    restart = get_texture("restart")
    exit = get_texture("exit")
    draw_texture(restart, 1050, 900, WHITE)
    draw_texture(exit, 1490, 900, WHITE)
    mpos = get_mouse_position()
    if check_collision_point_rec(mpos, Rectangle(1050, 900, restart.width, restart.height)):
        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
            board.reset_board()
            last_timer_update = 0.0
            STARTING_TIME = 600.0  # 10 minutes in seconds
            white_time = STARTING_TIME
            black_time = STARTING_TIME
            active_timer = None  # "white" or "black"

    if check_collision_point_rec(mpos, Rectangle(1490, 900, exit.width, exit.height)):
        if is_mouse_button_pressed(MOUSE_LEFT_BUTTON):
            close_window()
