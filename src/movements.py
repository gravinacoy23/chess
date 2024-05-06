from src.rules import Rules
from copy import deepcopy


class Movements:
    def __init__(self) -> None:
        self.selected_piece = None
        self.selected_piece_pos = None
        self.selected_square_owner = None
        self.selected_square = None
        self.previous_pos = None
        self.check_turn = None
        self.turn = "White"
        self.move_log_white = list()
        self.move_log_black = list()
        self.piece_is_captured = False
        self._color_slice = slice(None, 5)
        self._piece_slice = slice(6, None)
        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)
        self.possible_passant = False
        self.possible_passant_col = None
        self.passant_to_capture = None
        self.enpassant_counter = None
        self.counter = 0
        self.rules = Rules()

    def select_piece(self, board: list, mouse_pos: tuple) -> None:
        """Logic to select a piece depending on the state of the board (matrix) and the position on the mouse

        Args:
            board (Chess_board): Type defined on the board.py and has a list of lists with the current state of the
            board
            mouse_pos (Tuple): defined on the main.py
        """
        clicked_row, clicked_col = self._convert_mouse_pos_to_board(mouse_pos)
        if board[clicked_col][clicked_row] is not None:
            self.selected_piece = board[clicked_col][clicked_row]
            self.selected_piece_pos = (clicked_col, clicked_row)

    def select_square(self, board: list, mouse_pos: tuple) -> None:
        """Takes care of selecting a square that we clicked, an empty square thanks to the logic of the main.py file.

        Args:
            board (Chess_board): defined on the board.py
            mouse_pos (Tuple): defined on the main.py
        """
        clicked_row, clicked_col = self._convert_mouse_pos_to_board(mouse_pos)
        self.selected_square_owner = board[clicked_col][clicked_row]
        self.selected_square = (clicked_col, clicked_row)

    @staticmethod
    def _convert_mouse_pos_to_board(position: tuple) -> tuple:
        """Math expression that converts the position of the mouse to one of the positions in the 2d array board

        Args:
            position (Tuple): Position of the mouse, defined on main.py

        Returns:
            tuple: return a tuple with the conversion of the position of the mouse.
        """
        row, col = position
        cell_width = 83
        cell_height = 87
        row = min(max(0, (row - 198) // cell_height), 7)
        col = min(max(0, (col - 52) // cell_width), 7)
        return row, col

    def _regular_movement(self, board: list) -> None:
        """The purpose of this function is to make a regular move, AKA not a capture.

        Args:
            board (list): Current state of the board
        """
        row_init, col_init = self.selected_piece_pos
        row_to_move, col_to_move = self.selected_square
        board[row_to_move][col_to_move] = self.selected_piece
        board[row_init][col_init] = None
        
        if self.rules.castle is not None:
            board[self.selected_piece_pos[0]][self.selected_piece_pos[1] + self.rules.rook_pos] = None
            board[self.selected_piece_pos[0]][self.selected_square[1] + self.rules.rook_direction] \
                = f"{self.selected_piece[self._color_slice]} Rook"
        
        if not self.rules.en_passant:
            self.convert_move_to_chess_notation(
                self.selected_piece_pos,
                self.selected_square,
                self.selected_piece,
                self.piece_is_captured,
            )
        if self.selected_piece[self._piece_slice] == "Pawn":
            if (
                row_to_move + 2 == row_init
                or row_to_move - 2 == row_init
            ):
                self.possible_passant = True
                self.enpassant_counter = self.counter
                self.possible_passant_col = col_init
        else:
            self.possible_passant = False

        if self.counter != self.enpassant_counter:
            self.possible_passant = False

        self.selected_piece_passant = self.selected_piece
        self.selected_piece = None
        self.selected_square_owner = None
        if self.turn == "White":
            self.turn = "Black"
        else:
            self.turn = "White"

    def _capture(self, board: list) -> None:
        """The purpose of this function is to successfully handle capture.

        Args:
            board (list): Current state of the board
        """
        self.piece_is_captured = True
        row_init, col_init = self.selected_piece_pos
        row_to_move, col_to_move = self.selected_square
        board[row_to_move][col_to_move] = self.selected_piece
        board[row_init][col_init] = None
        self.convert_move_to_chess_notation(
            self.selected_piece_pos,
            self.selected_square,
            self.selected_piece,
            self.piece_is_captured,
        )
        self.selected_piece = None
        self.selected_square_owner = None
        self.piece_is_captured = False
        if self.turn == "White":
            self.turn = "Black"
        else:
            self.turn = "White"

    def _passant(self, board: list) -> None:
        """Handles En passant captures

        Args:
            board (list): Current state of the board
        """
        self.selected_piece = self.selected_piece_passant
        row_to_move, col_to_move = self.selected_square
        if self.selected_piece[self._color_slice] == "White":
            board[row_to_move + 1][col_to_move] = None
        if self.selected_piece[self._color_slice] == "Black":
            board[row_to_move - 1][col_to_move] = None
        self.convert_move_to_chess_notation(
            self.selected_piece_pos,
            self.selected_square,
            self.selected_piece,
            piece_is_captured=True,
        )
        self.selected_piece = None
        self.rules.en_passant = False

    def _check(self, board: list, king_pos: tuple) -> bool:
        """This function checks whether the king is currently on check given the king pos and a given board. It calls
        the define valid moves function for all the pieces in the board and sees if the king pos is contained in any of
        the valid moves.

        Args:
            board (list): 2d array with the current state of the board
            king_pos (tuple): Position of the king on the board

        Returns:
            bool: True if the king is in check, False otherwise
        """
        for row in range(0, 8):
            for col in range(0, 8):
                if board[row][col] is None:
                    continue
                self.rules.define_valid_moves(
                    board[row][col],
                    (row, col),
                    king_pos,
                    board,
                    self._color_slice,
                    self._piece_slice,
                    self.possible_passant,
                    self.possible_passant_col,
                    self.check_turn,
                    checking=True
                )
                if self.rules.valid_move(king_pos):
                    return True
        return False
        
    def _out_of_check(self, board: list, king_pos: tuple) -> bool:
        """This function checks if after a given move the king is out of check, making a copy of the board and a copy of
        the king pos

        Args:
            board (list): 2d array with the current state of the board
            king_pos (tuple): Position of the king on the board

        Returns:
            bool: True if the move puts the king to safety, false otherwise
        """
        board_check = deepcopy(board)
        king_pos_copy = deepcopy(king_pos)
        
        if self.selected_piece[self._piece_slice] == 'King':
            king_pos_copy = self.selected_square
        
        board_check[self.selected_piece_pos[0]][self.selected_piece_pos[1]] = None
        board_check[self.selected_square[0]][self.selected_square[1]] = self.selected_piece
        return False if self._check(board_check, king_pos_copy) else True
        
    def move_piece(self, board: list) -> None:
        """This contains the logic to move a piece somewhat raw, very few rules.
        rules included: The turn of the player, you can only play on your turn. You can not move the piece to the same
        square that the piece is (for some reason this was deleting the pieces)
        If you are going to move the piece to a square with another piece it cannot be from the same color. this
        function does allow captures but does not have any rule on how to prevent an illegal capture.

        Args:
            board (List): Array of arrays.
        """
        checking = False
        if self.turn == 'White':
            self.check_turn = 'Black'
            if self._check(board, self.white_king_pos):
                checking = True
                if not self._out_of_check(board, self.white_king_pos):
                    return
        else:
            self.check_turn = 'White'
            if self._check(board, self.black_king_pos):
                checking = True
                if not self._out_of_check(board, self.black_king_pos):
                    return
        
        self.rules.define_valid_moves(
            self.selected_piece,
            self.selected_piece_pos,
            self.selected_square,
            board,
            self._color_slice,
            self._piece_slice,
            self.possible_passant,
            self.possible_passant_col,
            self.turn,
            checking,
        )
        if self.rules.valid_move(self.selected_square):
            if (
                self.turn == "White"
                and self.selected_piece[self._color_slice] == "White"
            ) or (
                self.turn == "Black"
                and self.selected_piece[self._color_slice] == "Black"
            ):
                # if self.selected_piece_pos == self.selected_square:
                #     self.selected_piece = None
                #     self.selected_square_owner = None
                
                if self.selected_square_owner is None:
                    if self.turn == 'White':
                        self.check_turn = 'Black'
                        if not self._out_of_check(board, self.white_king_pos):
                            return
                    else:
                        self.check_turn = 'White'
                        if not self._out_of_check(board, self.black_king_pos):
                            return
                    if self.selected_piece == 'White King':
                        self.white_king_pos = self.selected_square
                    elif self.selected_piece == 'Black King':
                        self.black_king_pos = self.selected_square
                    self.counter += 1
                    self._regular_movement(board)
                elif (
                    self.selected_piece[self._color_slice]
                    != self.selected_square_owner[self._color_slice]
                ):
                    if self.turn == 'White':
                        self.check_turn = 'Black'
                        if not self._out_of_check(board, self.white_king_pos):
                            return
                    else:
                        self.check_turn = 'White'
                        if not self._out_of_check(board, self.black_king_pos):
                            return
                    if self.selected_piece == 'White King':
                        self.white_king_pos = self.selected_square
                    elif self.selected_piece == 'Black King':
                        self.black_king_pos = self.selected_square
                    self.counter += 1
                    self._capture(board)
                    return
                
                if self.rules.en_passant:
                    self._passant(board)

    def convert_move_to_chess_notation(
        self,
        init_square: tuple,
        final_square: tuple,
        selected_piece: str,
        piece_is_captured: bool,
    ) -> None:
        """In order to display on the screen the move on a chess notation created this function to convert the moves
        from the board coordinates to a chess notation, appending them
        to the move log list for both black and white.

        Args:
            init_square (tuple): To display some of the notation, specially in pawns
            final_square (tuple): for the notation to be accurate
            selected_piece (Str): Again, for the notation
            piece_is_captured (Bool): to determine if we should add an x between the piece and the final square ej. exe4
            (pawn from the E column capturing on the e4 square)
        """
        column_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]
        row_numbers = [8, 7, 6, 5, 4, 3, 2, 1]

        init_row, init_col = init_square
        final_row, final_col = final_square

        init_square_chess = column_letters[init_col] + str(row_numbers[init_row])
        final_square_chess = column_letters[final_col] + str(row_numbers[final_row])

        if piece_is_captured:
            if selected_piece[self._piece_slice] == "Pawn":
                if selected_piece[self._color_slice] == "White":
                    self.move_log_white.append(
                        f"{init_square_chess[0]}x{final_square_chess}"
                    )
                else:
                    self.move_log_black.append(
                        f"{init_square_chess[0]}x{final_square_chess}"
                    )
            else:
                if selected_piece[:5] == "White":
                    self.move_log_white.append(
                        f"{selected_piece[6]}x{final_square_chess}"
                    )
                else:
                    self.move_log_black.append(
                        f"{selected_piece[6]}x{final_square_chess}"
                    )
        elif selected_piece[self._piece_slice] == "Pawn":
            if selected_piece[self._color_slice] == "White":
                self.move_log_white.append(f"{final_square_chess}")
            else:
                self.move_log_black.append(f"{final_square_chess}")
        elif self.rules.castle is not None:
            if self.rules.castle == "Short":
                if selected_piece[self._color_slice] == "White":
                    self.move_log_white.append("O-O")
                else:
                    self.move_log_black.append("O-O")
            elif self.rules.castle == "Long":
                if self.selected_piece[self._color_slice] == "White":
                    self.move_log_white.append("O-O-O")
                else:
                    self.move_log_black.append("O-O-O")
            self.rules.castle = None
        else:
            if selected_piece[self._color_slice] == "White":
                self.move_log_white.append(
                    f"{selected_piece[6]}{final_square_chess}"
                )
            else:
                self.move_log_black.append(
                    f"{selected_piece[6]}{final_square_chess}"
                )
