from pyray import *
from raylib.enums import MouseButton
from player import get_current_player

UNITS = 124  # temp units for the scaling of the board
BORDER = 46
# these are custum colours cause why not
CREAM = Color(255, 253, 208, 255)
VI = Color(197, 27, 89, 255)
CAIT = Color(30, 50, 60, 255)
WOOD = Color(139, 69, 19, 255)

board_texture = None
sound_manager = dict()


class ChessBoard:

    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.state = {}
        self.dirs = {
            "up": (-1, 0),
            "down": (+1, 0),
            "left": (0, -1),
            "right": (0, 1),
            "top_left": (-1, -1),
            "top_right": (-1, 1),
            "bottom_left": (1, -1),
            "bottom_right": (1, 1),
            "up_left": (-2, -1),
            "up_right": (-2, 1),
            "down_left": (2, -1),
            "down_right": (2, 1),
            "left_up": (-1, -2),
            "left_down": (1, -2),
            "right_up": (-1, 2),
            "right_down": (1, 2),
        }
        self.selected = None
        self.check_state = False
        self.checkmate_state = False
        self.stalemate_state = False
        self.promotion = None
        self.promote_to = ""
        self.sound = False
        self.piece_captured = False
        self._initialize_empty_board()

    def draw_board(self):
        draw_texture(board_texture, 1, -2, WHITE)

    def draw_positions(self):
        for i in range(8):
            for j in range(8):
                draw_text("({},{})".format(j, i), i*UNITS +
                          BORDER, j*UNITS + BORDER, 10, RED)

    def _initialize_empty_board(self):
        for i in range(8):
            for j in range(8):
                self.state[(i, j)] = None


def initializeBoardTexture():
    global board_texture
    board_texture = load_texture("assets/board_full.png")


def initializeSounds():
    global sound_manager

    sound_manager = {
        "check": load_sound("assets/sounds/check.mp3"),
        "checkmate": load_sound("assets/sounds/checkmate.mp3"),
        "stalemate": load_sound("assets/sounds/stalemate.mp3"),
        "move": load_sound("assets/sounds/move.mp3"),
        "capture1": load_sound("assets/sounds/capture.mp3"),
        "capture2": load_sound("assets/sounds/Lost.mp3"),
        "capture3": load_sound("assets/sounds/yeah_boy.mp3"),
        "capture4": load_sound("assets/sounds/goofy_rizz.mp3")
    }


def get_selected_piece(board):
    m_pos = get_mouse_position()
    m_x, m_y = int((m_pos.x - BORDER) //
                   UNITS), int((m_pos.y - BORDER) // UNITS)

    if is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT):
        if board.selected is None:
            piece = board.state.get((m_y, m_x))
            if piece is not None and piece.color == get_current_player(board).color:
                piece.dragging = True
                board.selected = piece

    elif is_mouse_button_released(MouseButton.MOUSE_BUTTON_LEFT) and board.selected:
        piece = board.selected
        piece.dragging = False
        board.selected = None
        piece.move(m_y, m_x, board)


def listen_sounds(board):
    if board.sound:
        if board.checkmate_state:
            play_sound(sound_manager["checkmate"])
        elif board.stalemate_state:
            play_sound(sound_manager["stalemate"])
        elif board.check_state:
            play_sound(sound_manager["check"])
        elif board.piece_captured:
            play_sound(sound_manager[f"capture{get_random_value(1, 4)}"])
            board.piece_captured = False
        else:
            play_sound(sound_manager["move"])
        board.sound = False
