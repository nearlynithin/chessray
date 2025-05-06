from pyray import *
import random

SCREEN_W = 1920 
SCREEN_H = 1080

# Sidebar dimensions and styling
BUTTON_WIDTH = 300
BUTTON_HEIGHT = 70
BUTTON_SPACING = 40
BUTTON_X = SCREEN_W - BUTTON_WIDTH - 40  # 40px from right edge
button_y_start = 150  # Vertical start
BUTTON_COLOR = LIGHTGRAY
BUTTON_HOVER = DARKGRAY

#timers
white_time = 0.0
black_time = 0.0
active_timer = None  # "white" or "black"
last_timer_update = 0.0

button_x = SCREEN_W - BUTTON_WIDTH - 60  # 60px from right edge
center_y = SCREEN_H = 1080 // 2 - ((BUTTON_HEIGHT * 2 + BUTTON_SPACING) // 2)
button_y_start = (SCREEN_H // 2) - ((BUTTON_HEIGHT * 2 + BUTTON_SPACING) // 2) # Updated Y-coordinate calculation for toggle_btn

# Define buttons as rectangles
new_game_btn = Rectangle(button_x, center_y, BUTTON_WIDTH, BUTTON_HEIGHT)
continue_btn = Rectangle(button_x, center_y + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT)
toggle_btn = Rectangle(BUTTON_X, button_y_start + 2 * (BUTTON_HEIGHT + BUTTON_SPACING), BUTTON_WIDTH, BUTTON_HEIGHT) #timer button 

promotion_choices = ["Queen", "Rook", "Bishop", "Knight"]
PROMOTION_WIDTH = 500
PROMOTION_HEIGHT = 300


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
        # Dimmed background
        draw_rectangle(0, 0, get_screen_width(),
                       get_screen_height(), Color(0, 0, 0, 100))

        # Popup box
        draw_rectangle_rec(promotion_rect, Color(
            245, 245, 245, 240))  # light, almost opaque
        draw_rectangle_lines_ex(promotion_rect, 4, DARKGRAY)

        draw_text("Promote to:", int(promotion_rect.x + 20),
                  int(promotion_rect.y + 20), 24, BLACK)

        for i, name in enumerate(promotion_choices):
            btn_rect = Rectangle(
                promotion_rect.x + 30 + i * 90,
                promotion_rect.y + 80,
                80, 40
            )
            hovered = check_collision_point_rec(mouse_pos, btn_rect)
            draw_rectangle_rec(btn_rect, DARKGRAY if hovered else LIGHTGRAY)
            draw_text(name, int(btn_rect.x + 10),
                      int(btn_rect.y + 10), 16, BLACK)

            if hovered and mouse_clicked:
                board.promote_to = name.lower()

# change name later
def draw_sidebar_ui():
    global white_time, black_time, active_timer, last_timer_update

    mouse_pos = get_mouse_position()
    mouse_clicked = is_mouse_button_pressed(MOUSE_LEFT_BUTTON)

    if draw_button(new_game_btn, "New Game", mouse_pos, mouse_clicked):
        # Reset both timers
        white_time = 0.0
        black_time = 0.0
        active_timer = "white"  # White starts first in chess
        last_timer_update = get_time()
        return "new_game"
    
    if draw_button(continue_btn, "Continue", mouse_pos, mouse_clicked):
        return "continue"

    if draw_button(toggle_btn, "Switch Turn", mouse_pos, mouse_clicked):
        return "toggle_turn"

    return None


def update_timers():
    global white_time, black_time, active_timer, last_timer_update

    now = get_time()
    delta = now - last_timer_update
    last_timer_update = now

    if active_timer == "white":
        white_time += delta
    elif active_timer == "black":
        black_time += delta

def draw_timers():
    def format_time(t):
        minutes = int(t // 60)
        seconds = int(t % 60)
        return f"{minutes:02}:{seconds:02}"

    # Set the X coordinate to move the timer to the right side
    right_x = SCREEN_W - 250  # 250px from the right edge

    draw_text(f"White: {format_time(white_time)}", right_x, 50, 30, BLACK)
    draw_text(f"Black: {format_time(black_time)}", right_x, 100, 30, BLACK)

def draw_button(rect, text, mouse_pos, mouse_clicked):
    hovered = check_collision_point_rec(mouse_pos, rect)
    draw_rectangle_rec(rect, BUTTON_HOVER if hovered else BUTTON_COLOR)
    draw_text(text, int(rect.x + 20), int(rect.y + 15), 20, BLACK)

    return hovered and mouse_clicked

def toggle_timer():
    global active_timer, last_timer_update
    if active_timer == "white":
        active_timer = "black"
    else:
        active_timer = "white"
    last_timer_update = get_time()  # reset to avoid time jump

# ignore this for now
def draw_scanlines():
    for i in range(0, get_screen_height(), 4):
        draw_rectangle(0, i, get_screen_width(), 2, Color(0, 0, 0, 40))


def draw_vhs_tint():
    draw_rectangle(0, 0, get_screen_width(),
                   get_screen_height(), Color(255, 0, 50, 20))


def draw_vhs_noise():
    for i in range(30):
        x = random.randint(0, get_screen_width())
        y = random.randint(0, get_screen_height())
        draw_pixel(x, y, Color(255, 255, 255, 100))

# movement here


scanline_offset = 0  # global or class-level variable


def draw_scanlines_moving():
    global scanline_offset
    scanline_offset = (scanline_offset + 1) % 4  # move slowly
    for y in range(0, get_screen_height(), 4):
        draw_rectangle(0, y + scanline_offset,
                       get_screen_width(), 2, Color(0, 0, 0, 40))


def draw_vhs_noise_moving():
    for _ in range(30):
        x = random.randint(0, get_screen_width())
        y = random.randint(0, get_screen_height())
        alpha = random.randint(60, 150)  # Flickering brightness
        draw_pixel(x, y, Color(255, 255, 255, alpha))
