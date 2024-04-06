from board import Chess_board


class Movements:
    def __init__(self) -> None:
        self.selected_piece = None
        self.selected_piece_pos = None
        self.selected_square_owner = None
        self.selected_square = None
        self.previous_pos = None
        self.turn = "White"
        self.chess_board = Chess_board()
        self.move_log_white = list()
        self.move_log_black = list()
        self.piece_is_captured = False

    def select_piece(self, board, mouse_pos):
        """Logic to select a piece depending on the state of the board (matrix) and the position on the mouse

        Args:
            board (Chess_board): Type defined on the board.py and has a list of lists with the current state of the board
            mouse_pos (Tuple): defined on the main.py
        """
        clicked_row, clicked_col = self._convert_mousepos_to_board(mouse_pos)
        if board[clicked_col][clicked_row] is not None:
            self.selected_piece = board[clicked_col][clicked_row]
            self.selected_piece_pos = (clicked_col, clicked_row)

    def select_square(self, board, mouse_pos):
        """Takes care of selecting a square that we clicked, an empty square thanks to the logic of the main.py file.

        Args:
            board (Chess_board): defined on the board.py
            mouse_pos (Tuple): defined on the main.py
        """
        clicked_row, clicked_col = self._convert_mousepos_to_board(mouse_pos)
        self.selected_square_owner = board[clicked_col][clicked_row]
        self.selected_square = (clicked_col, clicked_row)

    def _convert_mousepos_to_board(self, position):
        """This is a match case statement to match the position of the mouse to a row col so that we can work with it on the functions of this class.

        Args:
            position (Tuple): Position of the mouse, defined on main.py

        Returns:
            tuple: return a tuple with the conversion of the position of the mouse.
        """
        row, col = position

        match row:
            case _ if 198 <= row < 285:
                row = 0
            case _ if 285 <= row < 373:
                row = 1
            case _ if 373 <= row < 460:
                row = 2
            case _ if 460 <= row < 547:
                row = 3
            case _ if 547 <= row < 635:
                row = 4
            case _ if 635 <= row < 721:
                row = 5
            case _ if 721 <= row < 808:
                row = 6
            case _ if 808 <= row < 896:
                row = 7

        match col:
            case _ if 52 <= col < 135:
                col = 0
            case _ if 135 <= col < 220:
                col = 1
            case _ if 220 <= col < 304:
                col = 2
            case _ if 304 <= col < 388:
                col = 3
            case _ if 388 <= col < 473:
                col = 4
            case _ if 473 <= col < 556:
                col = 5
            case _ if 556 <= col < 640:
                col = 6
            case _ if 640 <= col < 724:
                col = 7

        return row, col

    def move_piece(self, board, selecting_piece):
        """This contains the logic to move a piece somewhat raw, very few rules.
        rules included: The turn of the player, you can only play on your turn. You can not move the piece to the same square that the piece is (for some reason this was deleting the pieces)
        If you are going to move the piece to a square with another piece it cannot be from the same color. this function does allow captures but does not have any rule on how to prevent an
        illegal capture.

        Args:
            board (_type_): _description_
        """
        if (self.turn == "White" and self.selected_piece[0:5] == "White") or (
            self.turn == "Black" and self.selected_piece[0:5] == "Black"
        ):
            if self.selected_piece_pos != self.selected_square:
                if self.selected_square_owner == None:
                    row_init, col_init = self.selected_piece_pos
                    row_to_move, col_to_move = self.selected_square
                    board[row_to_move][col_to_move] = self.selected_piece
                    self.convert_move_to_chess_notation(self.selected_piece_pos, self.selected_square, self.selected_piece, self.piece_is_captured)
                    board[row_init][col_init] = None
                    self.selected_piece = None
                    if self.turn == "White":
                        self.turn = "Black"
                    else:
                        self.turn = "White"
                elif self.selected_piece[0:5] != self.selected_square_owner[0:5]:
                    self.piece_is_captured = True
                    row_init, col_init = self.selected_piece_pos
                    row_to_move, col_to_move = self.selected_square
                    board[row_to_move][col_to_move] = self.selected_piece
                    self.convert_move_to_chess_notation(self.selected_piece_pos, self.selected_square, self.selected_piece, self.piece_is_captured)
                    board[row_init][col_init] = None
                    self.selected_piece = None
                    if self.turn == "White":
                        self.turn = "Black"
                    else:
                        self.turn = "White"
                else:
                    self.selected_piece = None
                    selecting_piece = True

    def convert_move_to_chess_notation(self, init_square, final_square, selected_piece, piece_is_captured):
        column_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        row_numbers = [8,7,6,5,4,3,2,1]

        init_row, init_col = init_square
        final_row, final_col = final_square

        init_square_chess = column_letters[init_col]+str(row_numbers[init_row])
        final_square_chess = column_letters[final_col]+str(row_numbers[final_row])

        if piece_is_captured: 
            if selected_piece[6:] == 'Pawn': 
                if selected_piece [:5] == 'White':
                    self.move_log_white.append(f'{init_square_chess[0]}x{final_square_chess}')
                else:
                    self.move_log_black.append(f'{init_square_chess[0]}x{final_square_chess}')
            else: 
                if selected_piece[:5] == 'White':
                    self.move_log_white.append(f'{selected_piece[6]}x{final_square_chess}')
                else:
                    self.move_log_black.append(f'{selected_piece[6]}x{final_square_chess}')
        else:
            if selected_piece[6:] == 'Pawn': 
                if selected_piece[:5] == 'White':
                    self.move_log_white.append(f"{final_square_chess}")
                else:
                    self.move_log_black.append(f"{final_square_chess}")
            else: 
                if selected_piece[:5] == 'White':
                    self.move_log_white.append(f"{selected_piece[6]}{final_square_chess}")
                else:
                    self.move_log_black.append(f"{selected_piece[6]}{final_square_chess}")