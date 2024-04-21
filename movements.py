from rules import Rules


class Movements:
    def __init__(self) -> None:
        self.selected_piece = None
        self.selected_piece_pos = None
        self.selected_square_owner = None
        self.selected_square = None
        self.previous_pos = None
        self.turn = "White"
        self.move_log_white = list()
        self.move_log_black = list()
        self.piece_is_captured = False
        self._color_slice = slice(None, 5)
        self._piece_slice = slice(6, None)
        self.possible_passant = False
        self.possible_passant_col = None
        self.passant_to_capture = None
        self.counter = 0
        self.rules = Rules()

    def select_piece(self, board: list, mouse_pos: tuple) -> None:
        """Logic to select a piece depending on the state of the board (matrix) and the position on the mouse

        Args:
            board (Chess_board): Type defined on the board.py and has a list of lists with the current state of the board
            mouse_pos (Tuple): defined on the main.py
        """
        clicked_row, clicked_col = self._convert_mousepos_to_board(mouse_pos)
        if board[clicked_col][clicked_row] is not None:
            self.selected_piece = board[clicked_col][clicked_row]
            self.selected_piece_pos = (clicked_col, clicked_row)

    def select_square(self, board: list, mouse_pos: tuple) -> None:
        """Takes care of selecting a square that we clicked, an empty square thanks to the logic of the main.py file.

        Args:
            board (Chess_board): defined on the board.py
            mouse_pos (Tuple): defined on the main.py
        """
        clicked_row, clicked_col = self._convert_mousepos_to_board(mouse_pos)
        self.selected_square_owner = board[clicked_col][clicked_row]
        self.selected_square = (clicked_col, clicked_row)

    def _convert_mousepos_to_board(self, position: tuple) -> tuple:
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

    def move_piece(self, board: list) -> None:
        """This contains the logic to move a piece somewhat raw, very few rules.
        rules included: The turn of the player, you can only play on your turn. You can not move the piece to the same square that the piece is (for some reason this was deleting the pieces)
        If you are going to move the piece to a square with another piece it cannot be from the same color. this function does allow captures but does not have any rule on how to prevent an
        illegal capture.

        Args:
            board (List): Array of arrays.
        """
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
        )
        if self.rules.valid_move(self.selected_square):
            if (
                self.turn == "White"
                and self.selected_piece[self._color_slice] == "White"
            ) or (
                self.turn == "Black"
                and self.selected_piece[self._color_slice] == "Black"
            ):
                self.counter += 1
                if self.selected_piece_pos != self.selected_square:
                    if self.selected_square_owner == None:
                        row_init, col_init = self.selected_piece_pos
                        row_to_move, col_to_move = self.selected_square
                        board[row_to_move][col_to_move] = self.selected_piece
                        board[row_init][col_init] = None
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
                        selected_piece_passant = self.selected_piece
                        self.selected_piece = None
                        self.selected_square_owner = None
                        if self.turn == "White":
                            self.turn = "Black"
                        else:
                            self.turn = "White"
                    elif (
                        self.selected_piece[self._color_slice]
                        != self.selected_square_owner[self._color_slice]
                    ):
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
                        return
                    if self.rules.en_passant:

                        self.piece_is_captured == True
                        self.selected_piece = selected_piece_passant
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

                else:
                    self.selected_piece = None
                    self.selected_square_owner = None
                    selecting_piece = True

    def convert_move_to_chess_notation(
        self,
        init_square: tuple,
        final_square: tuple,
        selected_piece: str,
        piece_is_captured: bool,
    ) -> None:
        """In order to display on the screen the move on a chess notation created this function to convert the moves from the board coordinates to a chess notation, appending them
        to the movelog list for both black and white.

        Args:
            init_square (tupple): To disolay some of the notation, specially in pawns
            final_square (tupple): for the notation to be accurate
            selected_piece (Str): Again, for the notation
            piece_is_captured (Bool): to determine if we should add an x beetween the piece and the final square ej. exe4 (pawn from the E column capturing on the e4 square)
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
        else:
            if selected_piece[self._piece_slice] == "Pawn":
                if selected_piece[self._color_slice] == "White":
                    self.move_log_white.append(f"{final_square_chess}")
                else:
                    self.move_log_black.append(f"{final_square_chess}")
            else:
                if selected_piece[:5] == "White":
                    self.move_log_white.append(
                        f"{selected_piece[6]}{final_square_chess}"
                    )
                else:
                    self.move_log_black.append(
                        f"{selected_piece[6]}{final_square_chess}"
                    )
