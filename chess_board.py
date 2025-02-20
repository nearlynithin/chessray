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
        # this square size btw to calc position of the each block
        SQ = 90
        # these are custum colours cause why not  
        CREAM = Color(255, 253, 208, 255)
        VI = Color(197, 27, 89, 255)
        CAIT = Color(30, 20, 60, 255)
        WOOD = Color(139, 69, 19, 255)
        
        for w in range(8):
            for b in range(8):
                x = b * SQ
                y = w * SQ
                color = WOOD if (w + b) % 2 else CREAM
                draw_rectangle(x, y, SQ, SQ, color)
        
