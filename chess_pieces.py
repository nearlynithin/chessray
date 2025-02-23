import pprint
from pyray import *
from chess_board import ChessBoard, UNITS


class Piece:
    def __init__(self, color, x, y, board):
        self.color = color
        self.x = x
        self.y = y
        self.moves = []
        self.t_color = WHITE
        self.board = board  # Store reference to the board

    def move(self, x, y):
        if (x, y) in self.moves:
            # Update board state
            old_pos = (self.x, self.y)
            new_pos = (x, y)
            self.board.state[new_pos] = self
            self.board.state[old_pos] = None
            self.x = x
            self.y = y
            if isinstance(self, Pawn):
                self.first = False

    def get_position(self):
        return (self.x, self.y)

    def init_texture(self):
        pass


class Pawn(Piece):
    def __init__(self, color, x, y, board):
        super().__init__(color, x, y, board)
        self.first = True
        self.t_color = WHITE

    def get_moves(self):
        self.moves.clear()
        opponent_color = "black" if self.color == "white" else "white"

        if (self.color == "white"):
            dx, dy = self.board.dirs["up"]
            next_row = self.x + dx
            next_col = self.x + dy
            next_pos = (next_row, next_col)

            print(self.board.state.get(next_pos))

            if 0 <= next_row < 8 and 0 <= next_col < 8 and self.board.state.get(next_pos) is None:
                self.moves.append(next_pos)
                if self.first:
                    next_row = self.x + dx * 2
                    next_col = self.x + dy * 2
                    next_pos = (next_row, next_col)
                    if 0 <= next_row < 8 and 0 <= next_col < 8 and self.board.state.get(next_pos) is None:
                        self.moves.append(next_pos)

        if (self.color == "black"):
            dx, dy = self.board.dirs["down"]
            next_row = self.x + dx
            next_col = self.x + dy
            next_pos = (next_row, next_col)

            if 0 <= next_row < 8 and 0 <= next_col < 8 and self.board.state.get(next_pos) is None:
                self.moves.append(next_pos)
                if self.first:
                    next_row = self.x + dx * 2
                    next_col = self.x + dy * 2
                    next_pos = (next_row, next_col)
                    if 0 <= next_row < 8 and 0 <= next_col < 8 and self.board.state.get(next_pos) is None:
                        self.moves.append(next_pos)


class Rook(Piece):
    def __init__(self, color, x, y, board):
        super().__init__(color, x, y, board)
        self.t_color = GREEN

    def get_moves(self):
        self.moves.clear()
        op_color = "black" if self.color == "white" else "white"

        for dir in ["up", "down", "left", "right"]:
            dr, dc = self.board.dirs[dir]
            step = 1

            while True:
                next_row = self.x + dr * step
                next_col = self.y + dc * step
                next_pos = (next_row, next_col)

                # Break if out of bounds
                if not (0 <= next_row < 8 and 0 <= next_col < 8):
                    break

                if self.board.state.get(next_pos) is None:
                    self.moves.append(next_pos)
                    step += 1
                    continue

                if self.board.state[next_pos].color == op_color:
                    self.moves.append(next_pos)
                break


class Bishop(Piece):
    def __init__(self, color, x, y, board):
        super().__init__(color, x, y, board)
        self.t_color = BLUE

    def get_moves(self):
        self.moves.clear()
        op_color = "black" if self.color == "white" else "white"

        for dir in ["top_left", "top_right", "bottom_left", "bottom_right"]:
            dx, dy = self.board.dirs[dir]
            step = 1
            while True:
                next_row = self.x + dx * step
                next_col = self.y + dy * step

                if not (0 <= next_row < 8 and 0 <= next_col < 8):
                    break

                next_pos = (next_row, next_col)

                if self.board.state[next_pos] is None:
                    self.moves.append(next_pos)
                    step += 1
                    continue

                if self.board.state[next_pos].color == op_color:
                    self.moves.append(next_pos)
                break


class Knight(Piece):
    def __init__(self, color, x, y, board):
        super().__init__(color, x, y, board)
        self.t_color = PURPLE

    def move(self, x, y):
        return super().move(x, y)

    def get_moves(self):
        self.moves.clear()
        op_color = "black" if self.color == "white" else "white"

        move_dir = ["up_left", "up_right", "down_left", 'down_right',
                    "left_up", "left_down", "right_up", "right_down"]
        for dir in move_dir:
            dx, dy = self.board.dirs[dir]
            next_row = self.x + dx
            next_col = self.y + dy

            next_pos = (next_row, next_col)
            if not (0 <= next_row < 8 and 0 <= next_col < 8):
                continue

            if self.board.state[next_pos] is None:
                self.moves.append(next_pos)
            else:
                if self.board.state[next_pos].color == op_color:
                    self.moves.append(next_pos)


class Queen(Piece):
    def __init__(self, color, x, y, board):
        super().__init__(color, x, y, board)

    def move(self, x, y):
        return super().move(x, y)

    def get_moves(self):
        self.moves.clear()
        op_color = "black" if self.color == "white" else "white"

        move_dir = ["up", "down", "left", "right", "top_left",
                    "top_right", "bottom_left", "bottom_right"]

        for dir in move_dir:
            step = 1
            dx, dy = self.board.dirs[dir]
            while True:
                next_row = self.x + dx * step
                next_col = self.y + dy * step

                if not (0 <= next_row < 8 and 0 <= next_col < 8):
                    break

                next_pos = (next_row, next_col)
                if self.board.state.get(next_pos) is None:
                    self.moves.append(next_pos)
                    step += 1
                    continue

                if self.board.state.get(next_pos).color == op_color:
                    self.moves.append(next_pos)
                break


class King(Piece):
    def __init__(self, color, x, y, board):
        super().__init__(color, x, y, board)
        self.check = False

    def move(self, x, y):
        return super().move(x, y)

    def get_moves(self):
        self.moves.clear()
        op_color = "black" if self.color == "white" else "white"

        move_dir = ["up", "down", "left", "right", "top_left",
                    "top_right", "bottom_left", "bottom_right"]

        for dir in move_dir:
            dx, dy = self.board.dirs[dir]

            next_row = self.x + dx
            next_col = self.y + dy

            if not (0 <= next_row < 8 and 0 <= next_col < 8):
                break

            next_pos = (next_row, next_col)

            if next_pos not in self.board.state:
                continue

            if self.board.state[next_pos] is None:
                self.moves.append(next_pos)
                continue

            if self.board.state[next_pos].color == op_color:
                self.moves.append(next_pos)


def offset(n):
    return n * UNITS + int(UNITS/2)


def initializePieces(board):
    for i in range(8):
        # Black Pawns
        board.state[(1, i)] = Pawn("black", 1, i, board)

        # White Pawns
        board.state[(6, i)] = Pawn("white", 6, i, board)

    # Rooks
    board.state[(0, 0)] = Rook("black", 0, 0, board)
    board.state[(7, 0)] = Rook("black", 7, 0, board)
    board.state[(0, 7)] = Rook("white", 0, 7, board)
    board.state[(7, 7)] = Rook("white", 7, 7, board)

    # Knights
    board.state[(0, 1)] = Knight("black", 0, 1, board)
    board.state[(0, 6)] = Knight("black", 0, 6, board)
    board.state[(7, 1)] = Knight("white", 7, 1, board)
    board.state[(7, 6)] = Knight("white", 7, 6, board)

    # Bishops
    board.state[(0, 2)] = Bishop("black", 0, 2, board)
    board.state[(0, 5)] = Bishop("black", 0, 5, board)
    board.state[(7, 2)] = Bishop("white", 7, 2, board)
    board.state[(7, 5)] = Bishop("white", 7, 5, board)

    # Queens
    board.state[(0, 3)] = Queen("black", 0, 3, board)
    board.state[(7, 3)] = Queen("white", 7, 3, board)

    # Kings
    board.state[(0, 4)] = King("black", 0, 4, board)
    board.state[(7, 4)] = King("white", 7, 4, board)

    pprint.pprint(board.state)


def initializeTextures(board):
    for _, piece in board.state.items():
        if piece is not None:
            piece.init_texture()
