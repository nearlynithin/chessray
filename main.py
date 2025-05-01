from pyray import *
from chess_board import ChessBoard, get_selected_piece, initializeBoardTexture
from chess_pieces import initializePieces, initializePieceTextures, drawPieces, update_all_piece_moves, is_checkmate, is_stalemate
from player import initializePlayers
from ui import draw_sidebar_ui, draw_vhs_noise, draw_vhs_tint, draw_scanlines, draw_scanlines_moving, draw_vhs_noise_moving

SCREEN_W = 1920
SCREEN_H = 1080


class Game:

    def initialize(self):
        set_config_flags(ConfigFlags.FLAG_WINDOW_UNDECORATED |
                         ConfigFlags.FLAG_MSAA_4X_HINT)
        init_window(SCREEN_W, SCREEN_H, 'pyShatranj')
        # set_target_fps(60)

        initializePlayers(board)
        initializePieces(board)
        initializePieceTextures(board)
        initializeBoardTexture(board)

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
        update_all_piece_moves(board)
        is_checkmate(board)
        is_stalemate(board)
        if board.checkmate_state:
            print("CHECKMATE")
        elif board.stalemate_state:
            print("STALEMATE")
        elif board.check_state:
            print("CHECK")

    def generate_output(self):
        begin_drawing()
        clear_background(DARKGRAY)
        board.draw_board()
        drawPieces(board)

        action = draw_sidebar_ui()
        # if action == "new_game":
        #     print("Blitz clicked") # add logic here for stopwatch
        # elif action == "continue":
        #     print("Normal clicked") # add here also

        # draw_scanlines()
        # draw_scanlines_moving()
        # draw_vhs_tint()
        # draw_vhs_noise()
        # draw_vhs_noise_moving()
        draw_fps(20, 20)
        end_drawing()


if __name__ == '__main__':
    game = Game()
    board = ChessBoard()

    if (game.initialize()):
        game.run_loop()
    game.shutdown()
