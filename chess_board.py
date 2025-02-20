from pyray import *

UNITS = 5  # temp units for the scaling of the board
dirs = {
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
state = {}


class ChessBoard:

    def __init__(self):
        self.pieces = {}
        self.initialize_pieces()

    def initialize_pieces(self):
        pass

    def draw_board(self):
        draw_rectangle(int(40), int(40), 40, 40, WHITE)
        draw_rectangle(int(50), int(50), 40, 40, BLACK)
