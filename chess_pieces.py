import pprint
from pyray import *
from chess_board import UNITS, BORDER
from player import switch_turn, get_current_player, get_not_current_player
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

    def move(self, x, y, board):
        if (x, y) in self.moves:
            # Update board state
            old_pos = (self.x, self.y)
            new_pos = (x, y)
            self.board.state[new_pos] = self
            self.board.state[old_pos] = None
            self.x = x
            self.y = y
            switch_turn(board)
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
            d_rec = Rectangle(self.y * UNITS + BORDER,
                              self.x * UNITS + BORDER, UNITS, UNITS)
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
        self.is_castling = False
        self.first = True

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

            attackers = get_attack_pieces_at(next_pos, op_color, self.board)
            if len(attackers) > 0:
                continue

            if self.board.state[next_pos] is None:
                self.moves.append(next_pos)
                continue

            if self.board.state[next_pos].color == op_color:
                self.moves.append(next_pos)

    def is_under_check(self):
        return True if self.check else False


def offset(n):
    return n * UNITS + int(UNITS/2)


def initializePieces(board):
    initial_board(board)
    # straight_line_attack(board)
    # stalemate_test(board)


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


def update_all_piece_moves(board):
    for _, piece in board.state.items():
        if piece is not None:
            piece.get_moves()
            update_check(board)
            remove_illegal_moves(board)


def remove_illegal_moves(board):
    player = get_current_player(board)
    enemy = get_not_current_player(board)

    king_pos = player.king.get_position()
    enemy_pos = enemy.king.get_position()

    # Prevent adjacent kings
    adj = [(enemy_pos[0] + dx, enemy_pos[1] + dy)
           for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx or dy]
    player.king.moves = [m for m in player.king.moves if m not in adj]

    adj = [(king_pos[0] + dx, king_pos[1] + dy)
           for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dx or dy]
    enemy.king.moves = [m for m in enemy.king.moves if m not in adj]

    attacked_squares = set()
    for _, piece in board.state.items():
        if piece is None or piece.color == player.color:
            continue

        if isinstance(piece, Pawn):
            directions = ["top_left", "top_right"] if piece.color == "white" else [
                "bottom_left", "bottom_right"]
            for dir in directions:
                dx, dy = board.dirs[dir]
                attacked_squares.add((piece.x + dx, piece.y + dy))
        elif isinstance(piece, Knight):
            move_dir = ["up_left", "up_right", "down_left", 'down_right',
                        "left_up", "left_down", "right_up", "right_down"]
            for dir in move_dir:
                dx, dy = board.dirs[dir]
                attacked_squares.add((piece.x + dx, piece.y + dy))
        elif isinstance(piece, King):
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx or dy:
                        attacked_squares.add((piece.x + dx, piece.y + dy))
        else:
            attacked_squares.update(piece.moves)

    player.king.moves = [
        m for m in player.king.moves if m not in attacked_squares]

    for _, piece in board.state.items():
        if piece is None or piece.color != enemy.color:
            continue

        path = get_attack_path(piece.get_position(), king_pos)
        if not path:
            continue

        if not piece_can_attack_through(piece, path):
            continue

        blockers = [p for _, p in board.state.items(
        ) if p and p.get_position() in path]
        if len(blockers) == 1 and blockers[0].color == player.color:
            pinned = blockers[0]
            pinned.moves = [
                m for m in pinned.moves if m in path or m == king_pos]
        if len(blockers) == 0:
            path = get_range(piece, board)
            print(piece, piece.color, "Path : ", path)
            for move in player.king.moves:
                if move in path:
                    player.king.moves.remove(move)


def piece_can_attack_through(piece, path):
    if not path:
        return False

    dx = path[0][0] - piece.x
    dy = path[0][1] - piece.y

    if isinstance(piece, Rook):
        return dx == 0 or dy == 0
    elif isinstance(piece, Bishop):
        return abs(dx) == abs(dy)
    elif isinstance(piece, Queen):
        return dx == 0 or dy == 0 or abs(dx) == abs(dy)
    else:
        return False


def get_range(piece, board):
    path = []

    if isinstance(piece, Queen):
        directions = [
            board.dirs["up"], board.dirs["down"], board.dirs["left"], board.dirs["right"],
            board.dirs["top_left"], board.dirs["top_right"],
            board.dirs["bottom_left"], board.dirs["bottom_right"]
        ]
    elif isinstance(piece, Rook):
        directions = [
            board.dirs["up"], board.dirs["down"],
            board.dirs["left"], board.dirs["right"]
        ]
    elif isinstance(piece, Bishop):
        directions = [
            board.dirs["top_left"], board.dirs["top_right"],
            board.dirs["bottom_left"], board.dirs["bottom_right"]
        ]
    else:
        return path

    for dx, dy in directions:
        x, y = piece.x, piece.y
        while True:
            x += dx
            y += dy
            if not (0 <= x < 8 and 0 <= y < 8):
                break
            path.append((x, y))

    return path


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
            draw_circle(x + BORDER, y + BORDER, 10, GREEN)


def update_check(board):
    for player in [board.player1, board.player2]:
        for _, piece in board.state.items():
            if piece is not None:
                if piece.color != player.king.color:
                    if player.king.get_position() in piece.moves:
                        player.attack = piece
                        player.king.check = True
                        board.check_state = True
                        return True
                    else:
                        player.attack = None
                        player.king.check = False
                        board.check_state = False
    return False


def is_checkmate(board):
    if not board.check_state:
        return False

    player = board.player1
    for p in [board.player1, board.player2]:
        if p.king.is_under_check():
            player = p

    king = player.king
    king_pos = king.get_position()

    under_attack = False
    for move in king.moves:
        for _, piece in board.state.items():
            if piece is not None:
                if piece.color != king.color:
                    if move in piece.moves:
                        under_attack = True
                        break
        if not under_attack:
            return False

    attackers = get_attack_pieces_at(king_pos, player.attack.color, board)

    if len(attackers) > 1:
        return True

    if len(attackers) != 0:
        attacker = attackers[0]
        path = get_attack_path(attacker.get_position(), king_pos)

        for _, piece in board.state.items():
            if piece is not None:
                if piece.color != king.color or piece == king:
                    continue
                if attacker.get_position() in piece.moves:
                    return False
                for move in piece.moves:
                    if move in path:
                        return False
    board.checkmate_state = True
    return True


def is_stalemate(board):
    if board.check_state:
        return False

    player = get_current_player(board)

    empty = True
    for _, piece in board.state.items():
        if piece is not None:
            if piece.color == player.color:
                if piece.moves:
                    empty = False

    if empty:
        board.stalemate_state = True
        return True
    else:
        return False


def get_attack_pieces_at(position, attack_color, board):
    attackers = []
    for _, piece in board.state.items():
        if piece is not None:
            if piece.color == attack_color and position in piece.moves:
                attackers.append(piece)
    return attackers


def get_attack_path(start, end):
    start_x, start_y = start
    end_x, end_y = end

    dx = end_x - start_x
    dy = end_y - start_y

    path = []

    if dy == 0 and dx != 0:
        step = 1 if dx > 0 else -1
        path = [(x, start_y) for x in range(start_x + step, end_x, step)]

    # Vertical move
    elif dx == 0 and dy != 0:
        step = 1 if dy > 0 else -1
        path = [(start_x, y) for y in range(start_y + step, end_y, step)]

    elif abs(dx) == abs(dy) and dx != 0:
        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1
        path = [(start_x + i*step_x, start_y + i*step_y)
                for i in range(1, abs(dx))]
    return path


def stalemate_test(board):
    board.state[(1, 4)] = Pawn("black", 1, 4, board)
    board.state[(2, 5)] = Pawn("black", 2, 5, board)
    board.state[(1, 6)] = Pawn("black", 1, 6, board)
    board.state[(3, 7)] = Pawn("black", 3, 7, board)

    board.state[(6, 0)] = Pawn("white", 6, 0, board)
    board.state[(6, 1)] = Pawn("white", 6, 1, board)
    board.state[(4, 2)] = Pawn("white", 4, 2, board)
    board.state[(6, 3)] = Pawn("white", 6, 3, board)
    board.state[(6, 4)] = Pawn("white", 6, 4, board)
    board.state[(6, 5)] = Pawn("white", 6, 5, board)
    board.state[(6, 6)] = Pawn("white", 6, 6, board)
    board.state[(4, 7)] = Pawn("white", 4, 7, board)

    # Rooks
    board.state[(0, 7)] = Rook("black", 0, 7, board)
    board.state[(2, 7)] = Rook("black", 2, 7, board)
    board.state[(7, 0)] = Rook("white", 7, 0, board)
    board.state[(7, 7)] = Rook("white", 7, 7, board)

    # Knights
    board.state[(0, 6)] = Knight("black", 0, 6, board)
    board.state[(7, 1)] = Knight("white", 7, 1, board)
    board.state[(7, 6)] = Knight("white", 7, 6, board)

    # Bishops
    board.state[(0, 5)] = Bishop("black", 0, 5, board)
    board.state[(7, 2)] = Bishop("white", 7, 2, board)
    board.state[(7, 5)] = Bishop("white", 7, 5, board)

    # Queens
    board.state[(1, 7)] = Queen("black", 1, 7, board)
    board.state[(0, 2)] = Queen("white", 0, 2, board)

    # Kings
    board.state[(2, 6)] = King("black", 2, 6, board)
    board.state[(7, 4)] = King("white", 7, 4, board)
    board.player1.king = board.state[(7, 4)]
    board.player2.king = board.state[(2, 6)]


def pawn_attack(board):

    board.state[(5, 5)] = Pawn("white", 5, 5, board)
    board.state[(0, 7)] = Rook("black", 0, 7, board)
    board.state[(7, 0)] = Rook("white", 7, 0, board)
    board.state[(7, 7)] = Rook("white", 7, 7, board)

    # Kings
    board.state[(3, 3)] = King("black", 3, 3, board)
    board.state[(2, 6)] = King("white", 2, 6, board)
    board.player2.king = board.state[(3, 3)]
    board.player1.king = board.state[(2, 6)]


def straight_line_attack(board):
    board.state[(5, 5)] = Pawn("white", 5, 5, board)
    board.state[(0, 3)] = Rook("black", 0, 3, board)
    board.state[(7, 0)] = Rook("white", 7, 0, board)
    board.state[(7, 7)] = Rook("white", 7, 7, board)
    board.state[(5, 7)] = Queen("black", 5, 7, board)
    board.state[(0, 2)] = Queen("white", 0, 2, board)

    # Kings
    board.state[(3, 3)] = King("black", 3, 3, board)
    board.state[(2, 6)] = King("white", 2, 6, board)
    board.player2.king = board.state[(3, 3)]
    board.player1.king = board.state[(2, 6)]


def initial_board(board):
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
    board.player1.king = board.state[(7, 4)]
    board.player2.king = board.state[(0, 4)]

    pprint.pprint(board.state)
