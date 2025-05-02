class Player:
    def __init__(self, color):
        self.color = color
        self.is_turn = (color == "white")
        self.king = None
        self.attack = None
        self.captured_pieces = []
        self.castling = False

    def capture_piece(self, piece):
        self.captured_pieces.append(piece)


def initializePlayers(board):
    board.player1 = Player("white")
    board.player2 = Player("black")


def switch_turn(board):
    board.player1.is_turn = not board.player1.is_turn
    board.player2.is_turn = not board.player2.is_turn
    board.sound = True


def get_current_player(board):
    if board.player1.is_turn:
        return board.player1
    else:
        return board.player2


def get_not_current_player(board):
    if board.player1.is_turn:
        return board.player2
    else:
        return board.player1


def get_attack_player(board):
    if board.player1.attack is not None:
        return board.player1
    if board.player2.attack is not None:
        return board.player2
