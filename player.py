class Player:
    def __init__(self, color):
        self.color = color
        self.is_turn = (color == "white")
        self.captured_pieces = []

    def capture_piece(self, piece):
        self.captured_pieces.append(piece)