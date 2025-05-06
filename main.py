from pyray import *
from chess_board import ChessBoard, get_selected_piece, initializeBoardTexture,  initializeSounds, listen_sounds, draw_state
from chess_pieces import initializePieces, initializePieceTextures, drawPieces, update_all_piece_moves, is_checkmate, is_stalemate, pawn_promotion
from player import initializePlayers
from ui import *

SCREEN_W = 1920
SCREEN_H = 1080


class Game:

    def initialize(self):
        set_config_flags(ConfigFlags.FLAG_WINDOW_UNDECORATED |
                         ConfigFlags.FLAG_MSAA_4X_HINT)
        init_window(SCREEN_W, SCREEN_H, 'pyShatranj')
        init_audio_device()

        initializePlayers(board)
        initializePieces(board)
        initializePieceTextures(board)
        initializeBoardTexture()
        initializeSounds()

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
        pawn_promotion(board)

        update_timers()

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
        draw_promotion_popup(board)
        draw_state(board)
        listen_sounds(board)

        listen_timer(board)
        draw_fps(20, 20)
        draw_timer_texture()
        m_pos = get_mouse_position()
        draw_text(f"{m_pos.x},{m_pos.y}", int(
            m_pos.x + 10), int(m_pos.y + 10), 15, BLACK)
        draw_timers()
        draw_buttons(board)
        end_drawing()


if __name__ == '__main__':
    game = Game()
    board = ChessBoard()

    if (game.initialize()):
        game.run_loop()
    game.shutdown()
