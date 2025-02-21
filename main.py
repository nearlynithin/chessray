from pyray import *
from chess_board import ChessBoard, UNITS
from chess_pieces import initializePieces

SCREEN_W = 1280
SCREEN_H = 720


class Game:

    def initialize(self):
        init_window(SCREEN_W, SCREEN_H, 'pyShatranj')
        set_target_fps(60)

        initializePieces()

        if is_window_ready():
            return True

    def run_loop(self):
        while not window_should_close():
            self.process_input()
            self.update_game()
            self.generate_output()

    def shutdown(self):
        close_window()

    def process_input(self):
        pass

    def update_game(self):
        pass

    def generate_output(self):
        begin_drawing()
        clear_background(BLUE)
        draw_text("Konnichiwa", 30, 40, 30, WHITE)
        board.draw_board()
        board.drawPieces()
        end_drawing()


if __name__ == '__main__':
    game = Game()
    board = ChessBoard()

    if (game.initialize()):
        game.run_loop()
    game.shutdown()
