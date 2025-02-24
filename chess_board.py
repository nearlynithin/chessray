from pyray import *
import pprint

UNITS = 90  # temp units for the scaling of the board


class ChessBoard:

    def __init__(self):
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
        self._initialize_empty_board()
        pprint.pprint(self.state)

    def draw_board(self):
        # these are custum colours cause why not
        CREAM = Color(255, 253, 208, 255)
        VI = Color(197, 27, 89, 255)
        CAIT = Color(30, 20, 60, 255)
        WOOD = Color(139, 69, 19, 255)

        for w in range(8):
            for b in range(8):
                x = b * UNITS
                y = w * UNITS
                color = WOOD if (w + b) % 2 else CREAM
                draw_rectangle(x, y, UNITS, UNITS, color)

    def _initialize_empty_board(self):
        for i in range(8):
            for j in range(8):
                self.state[(i, j)] = None

    def drawPieces(self):
        for pos, piece in self.state.items():
            if piece is not None:
                y, x = pos
                x = (UNITS//2) + x * UNITS
                y = (UNITS//2) + y * UNITS
                draw_circle(x, y, 10, piece.t_color)
                # print(piece)

    def draw_moves(self):
        # pass
        for pos, piece in self.state.items():
            if piece is not None:
                piece.get_moves()
                for move in piece.moves:
                    y, x = move
                    x = (UNITS//2) + x * UNITS
                    y = (UNITS//2) + y * UNITS
                    draw_circle(x, y, 10, BLACK)
                print(
                    f"{type(piece).__name__} at {pos} has {len(piece.moves)} moves")
