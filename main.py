from pyray import *
from chess_board import ChessBoard, get_selected_piece
from chess_pieces import initializePieces, initializeTextures, drawPieces, is_check
from player import initializePlayers

SCREEN_W = 1280
SCREEN_H = 720


class Game:

    def initialize(self):
        init_window(SCREEN_W, SCREEN_H, 'pyShatranj')
        set_target_fps(60)

        initializePieces(board)
        initializeTextures(board)
        initializePlayers(board)

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
        get_selected_piece(board)

    def update_game(self):
        pass

    def generate_output(self):
        begin_drawing()
        clear_background(DARKGRAY)
        draw_text("Konnichiwa", 30, 40, 30, WHITE)
        board.draw_board()
        drawPieces(board)
        is_check(board)
        end_drawing()


if __name__ == '__main__':
    game = Game()
    board = ChessBoard()

    if (game.initialize()):
        game.run_loop()
    game.shutdown()
