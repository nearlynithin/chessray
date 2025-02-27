class Player:
    def __init__(self, color):
        self.color = color
        self.is_turn = (color == "white")
        self.captured_pieces = []

    def capture_piece(self, piece):
        self.captured_pieces.append(piece)


def initializePlayers(board):
    board.player1 = Player("white")
    board.player2 = Player("black")


def switch_turn(board):
    board.player1.is_turn = not board.player1.is_turn
    board.player2.is_turn = not board.player2.is_turn


def get_current_player(board):
    if board.player1.is_turn:
        return board.player1
    else:
        return board.player2
