import pprint
from pyray import *
from chess_board import ChessBoard, UNITS

piece_texture = None


class Piece:
    def __init__(self, color, x, y, board):
        self.color = color
        self.x = x
        self.y = y
        self.moves = []
        self.t_color = WHITE
        self.dragging = False
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

    def draw_piece(self):
        rec = get_texture_rec(self, self.color)
        if self.dragging:
            m_pos = get_mouse_position()
            m_x, m_y = m_pos.x, m_pos.y
            d_rec = Rectangle(m_x - UNITS//2, m_y - UNITS//2, UNITS, UNITS)
            draw_texture_pro(piece_texture, rec, d_rec, (0, 0), 0, WHITE)
        else:
            d_rec = Rectangle(self.y * UNITS, self.x * UNITS, UNITS, UNITS)
            draw_texture_pro(piece_texture, rec, d_rec, (0, 0), 0, WHITE)


class Pawn(Piece):
    def __init__(self, color, x, y, board):
        super().__init__(color, x, y, board)
        self.first = True
        self.t_color = WHITE

    def get_moves(self):
        self.moves.clear()
        opponent_color = "black" if self.color == "white" else "white"

        move_dir = ["up", "top_left", "top_right"] if self.color == "white" else [
            "down", "bottom_left", "bottom_right"]

        for dir in move_dir:
            dx, dy = self.board.dirs[dir]
            next_row = self.x + dx
            next_col = self.y + dy
            next_pos = (next_row, next_col)

            if 0 <= next_row < 8 and 0 <= next_col < 8:
                if self.board.state.get(next_pos) is None and dir == move_dir[0]:
                    self.moves.append(next_pos)
                    if self.first:
                        next_row = self.x + dx * 2
                        next_col = self.y + dy * 2
                        next_pos = (next_row, next_col)
                        if 0 <= next_row < 8 and 0 <= next_col < 8 and self.board.state.get(next_pos) is None:
                            self.moves.append(next_pos)
                elif self.board.state.get(next_pos) is not None and dir != move_dir[0]:
                    if self.board.state.get(next_pos).color == opponent_color:
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
                continue

            next_pos = (next_row, next_col)

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
    board.state[(0, 7)] = Rook("black", 0, 7, board)
    board.state[(7, 0)] = Rook("white", 7, 0, board)
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
    global piece_texture
    piece_texture = load_texture("assets/pieces.png")


def get_texture_rec(type, color):
    offs = 0
    if color == 'black':
        offs = 1
    if isinstance(type, Pawn):
        idx = 5
    elif isinstance(type, Rook):
        idx = 4
    elif isinstance(type, Knight):
        idx = 3
    elif isinstance(type, Bishop):
        idx = 2
    elif isinstance(type, Queen):
        idx = 1
    elif isinstance(type, King):
        idx = 0

    return Rectangle(idx * piece_texture.width//6, offs*piece_texture.height//2, piece_texture.width//6, piece_texture.height//2)


def drawPieces(board):
    for _, piece in board.state.items():
        if piece is not None:
            piece.draw_piece()
    piece = board.selected
    draw_moves(piece)


def draw_moves(piece):
    if piece is not None:
        for move in piece.moves:
            y, x = move
            x = (UNITS//2) + x * UNITS
            y = (UNITS//2) + y * UNITS
            draw_circle(x, y, 10, GREEN)
