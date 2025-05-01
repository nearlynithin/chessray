from pyray import *
import random

# Sidebar dimensions and styling
SIDEBAR_X = 8 * 90  # 8 tiles * 90 units per tile = 720
SIDEBAR_WIDTH = 560
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 30
BUTTON_COLOR = LIGHTGRAY
BUTTON_HOVER = DARKGRAY
VHS_DARK = Color(255, 0, 100, 20)

# Define buttons as rectangles
button_y_start = 150
new_game_btn = Rectangle(SIDEBAR_X + 50, button_y_start, BUTTON_WIDTH, BUTTON_HEIGHT)
continue_btn = Rectangle(SIDEBAR_X + 50, button_y_start + BUTTON_HEIGHT + BUTTON_SPACING, BUTTON_WIDTH, BUTTON_HEIGHT)

def draw_sidebar_ui():
    """Draw the grey sidebar and the buttons."""
    # Sidebar background
    draw_rectangle(SIDEBAR_X, 0, SIDEBAR_WIDTH, get_screen_height(), VHS_DARK)

    # Get mouse position
    mouse_pos = get_mouse_position()
    mouse_clicked = is_mouse_button_pressed(MOUSE_LEFT_BUTTON)

    # Draw and check buttons
    if draw_button(new_game_btn, "Blitz", mouse_pos, mouse_clicked):
        return "new_game"
    if draw_button(continue_btn, "Normal", mouse_pos, mouse_clicked):
        return "continue"

    return None

def draw_button(rect, text, mouse_pos, mouse_clicked):
    hovered = check_collision_point_rec(mouse_pos, rect)
    draw_rectangle_rec(rect, BUTTON_HOVER if hovered else BUTTON_COLOR)
    draw_text(text, int(rect.x + 20), int(rect.y + 15), 20, BLACK)

    return hovered and mouse_clicked

def draw_scanlines():
    for i in range(0, get_screen_height(), 4):
        draw_rectangle(0, i, get_screen_width(), 2, Color(0, 0, 0, 40))

def draw_vhs_tint():
    draw_rectangle(0, 0, get_screen_width(), get_screen_height(), Color(255, 0, 50, 20))

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
        draw_rectangle(0, y + scanline_offset, get_screen_width(), 2, Color(0, 0, 0, 40))

def draw_vhs_noise_moving():
    for _ in range(30):
        x = random.randint(0, get_screen_width())
        y = random.randint(0, get_screen_height())
        alpha = random.randint(60, 150)  # Flickering brightness
        draw_pixel(x, y, Color(255, 255, 255, alpha))

