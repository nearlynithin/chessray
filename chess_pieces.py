import chess_board as board


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
