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
                opponent_color = "black" if self.color == "white" else "white"
                if board.state[capture_pos].color == opponent_color:
                    self.moves.append(capture_pos)