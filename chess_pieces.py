import chess_board as board
from chess_board import UNITS


class Piece:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y
        self.moves = []

    def __del__(self):
        # destructor
        pass

    def move(self, x, y):
        if (x, y) in self.moves:
            self.x = x
            self.y = y
            if isinstance(self, Pawn):
                self.first = False

    def get_position(self):
        return (self.x, self.y)

    def init_texture(self):
        # method to be overridden in every Piece's class
        print("Initializing textures...")

    def highlight(self):
        pass

    def get_moves(self):
        pass


class Pawn(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.first = True

    def move(self, x, y):
        super().move(x, y)

    def get_moves(self):
        self.moves.clear()
        opponent_color = "black" if self.color == "white" else "white"
        dir = 1
        if self.color == "black":
            dir *= -1

        # Forward moves
        dx, dy = board.dirs["up"]
        forward_pos = (self.x + dx*dir, self.y + dy*dir)

        if forward_pos in board.state and board.state[forward_pos] is None:
            self.moves.append(forward_pos)
            if self.first:
                double_forward = (self.x + dx*2*dir, self.y + dy*2*dir)
                if double_forward in board.state and board.state[double_forward] is None:
                    self.moves.append(double_forward)

        # Capture moves
        for capture_dir in ["top_left", "top_right"]:
            dx, dy = board.dirs[capture_dir]
            capture_pos = (self.x + dx*dir, self.y + dy*dir)

            if capture_pos in board.state and board.state[capture_pos] is not None:
                if board.state[capture_pos].color == opponent_color:
                    self.moves.append(capture_pos)


class Rook(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def move(self, x, y):
        return super().move(x, y)

    def get_moves(self):
        self.moves.clear()
        op_color = "black" if self.color == "white" else "white"

        move_dir = ["up", "down", "left", "right"]
        for dir in move_dir:
            dx, dy = board.dirs[dir]
            step = 1
            while True:
                next_pos = (self.x + dx * step, self.y + dy * step)

                if next_pos not in board.state:
                    break

                if board.state[next_pos] is None:
                    self.moves.append(next_pos)
                    step += 1
                    continue

                if board.state[next_pos].color == op_color:
                    self.moves.append(next_pos)
                break


class Bishop(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def move(self, x, y):
        return super().move(x, y)

    def get_moves(self):
        self.moves.clear()
        op_color = "black" if self.color == "white" else "white"

        move_dir = ["top_left", "top_right", "bottom_left", "bottom_right"]
        for dir in move_dir:
            dx, dy = board.dirs[dir]
            step = 1
            while True:
                next_pos = (self.x + dx * step, self.y + dy * step)

                if next_pos not in board.state:
                    break

                if board.state[next_pos] is None:
                    self.moves.append(next_pos)
                    step += 1
                    continue

                if board.state[next_pos].color == op_color:
                    self.moves.append(next_pos)
                break


class Knight(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def move(self, x, y):
        return super().move(x, y)

    def get_moves(self):
        self.moves.clear()
        op_color = "black" if self.color == "white" else "white"

        move_dir = ["up_left", "up_right", "down_left", 'down_right',
                    "left_up", "left_down", "right_up", "right_down"]
        for dir in move_dir:
            dx, dy = board.dirs[dir]
            next_pos = (self.x + dx, self.y + dy)

            if next_pos not in board.state:
                continue

            if board.state[next_pos] is None:
                self.moves.append(next_pos)
            else:
                if board.state[next_pos].color == op_color:
                    self.moves.append(next_pos)


class Queen(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)

    def move(self, x, y):
        return super().move(x, y)

    def get_moves(self):
        self.moves.clear()
        op_color = "black" if self.color == "white" else "white"

        move_dir = ["up", "down", "left", "right", "top_left",
                    "top_right", "bottom_left", "bottom_right"]

        for dir in move_dir:
            step = 1
            dx, dy = board.dirs[dir]
            while True:
                next_pos = (self.x + dx * step, self.y + dy * step)

                if next_pos not in board.state:
                    break

                if board.state[next_pos] is None:
                    self.moves.append(next_pos)
                    step += 1
                    continue

                if board.state[next_pos].color == op_color:
                    self.moves.append(next_pos)
                    break


class King(Piece):
    def __init__(self, color, x, y):
        super().__init__(color, x, y)
        self.check = False

    def move(self, x, y):
        return super().move(x, y)

    def get_moves(self):
        self.moves.clear()
        op_color = "black" if self.color == "white" else "white"

        move_dir = ["up", "down", "left", "right", "top_left",
                    "top_right", "bottom_left", "bottom_right"]

        for dir in move_dir:
            dx, dy = board.state[dir]

            next_pos = (self.x + dx, self.y + dy)

            if next_pos not in board.state:
                continue

            if board.state[next_pos] is None:
                self.moves.append(next_pos)
                continue

            if board.state[next_pos].color == op_color:
                self.moves.append(next_pos)


def offset(n):
    return n * UNITS + int(UNITS/2)


def initializePieces():

    for i in range(8):
        # Black Pawns
        x = offset(i)
        y = offset(1)
        board.state[(x, y)] = Pawn("black", x, y)

        # White Pawns
        y = offset(6)
        board.state[(x, y)] = Pawn("white", x, y)

    # Rooks
    board.state[(offset(0), offset(0))] = Rook("black", offset(0), offset(0))
    board.state[(offset(7), offset(0))] = Rook("black", offset(7), offset(0))
    board.state[(offset(0), offset(7))] = Rook("white", offset(0), offset(7))
    board.state[(offset(7), offset(7))] = Rook("white", offset(7), offset(7))

    # Knights
    board.state[(offset(1), offset(0))] = Knight("black", offset(1), offset(0))
    board.state[(offset(6), offset(0))] = Knight("black", offset(6), offset(0))
    board.state[(offset(1), offset(7))] = Knight("white", offset(1), offset(7))
    board.state[(offset(6), offset(7))] = Knight("white", offset(6), offset(7))

    # Bishops
    board.state[(offset(2), offset(0))] = Bishop("black", offset(2), offset(0))
    board.state[(offset(5), offset(0))] = Bishop("black", offset(5), offset(0))
    board.state[(offset(2), offset(7))] = Bishop("white", offset(2), offset(7))
    board.state[(offset(5), offset(7))] = Bishop("white", offset(5), offset(7))

    # Queens
    board.state[(offset(3), offset(0))] = Queen("black", offset(3), offset(0))
    board.state[(offset(3), offset(7))] = Queen("white", offset(3), offset(7))

    # Kings
    board.state[(offset(4), offset(0))] = King("black", offset(4), offset(0))
    board.state[(offset(4), offset(7))] = King("white", offset(4), offset(7))


def initializeTextures():
    for _, pieces in board.state.items():
        pieces.init_texture()
