class Rules:
    def __init__(self) -> None:
        """initializes the list to pass as an argument on a function."""
        self.valid_moves = list()
        self.en_passant = False
        self.castle = None

    def _define_pawn_moves(
        self,
        selected_piece: str,
        selected_piece_row: int,
        selected_piece_col: int,
        selected_square_col: int,
        board: list,
        color_slice: slice,
        possible_passant: bool,
        possible_passant_col: int,
    ) -> None:
        """This method is used to determine the valid moves for a given pawn, whether a capture or a move forward.

        Args:
            selected_piece (str): a string containing the name of the piece ej. White pawn
            selected_piece_row (int): number of the row in which the piece currently is.
            selected_piece_col (int): number of the column in which the piece currently is.
            selected_square_col (int): column in which the selected square is (selected square to move)
            board (list): array of arrays.
            color_slice (slice): Contains a slice object that references the color of the piece string in format "White
            Pawn"
            possible_passant (bool): Bool that indicates if the en passant is possible in the next turn depending on the
            previous move
            possible_passant_col (int): The column in which the possible enpassant is located.
        """
        if selected_piece[color_slice] == "White":
            player_color = "White"
            direction = -1
            start_row = 6
            en_passant_row = 3
        else:
            player_color = "Black"
            direction = 1
            start_row = 1
            en_passant_row = 4

        if board[selected_piece_row + direction][selected_piece_col] is None:
            self.valid_moves.append(
                (selected_piece_row + direction, selected_piece_col)
            )
            if (
                selected_piece_row == start_row
                and board[selected_piece_row + 2 * direction][selected_piece_col]
                is None
            ):
                self.valid_moves.append(
                    (selected_piece_row + 2 * direction, selected_piece_col)
                )

        if (
            selected_square_col == selected_piece_col - 1
            or selected_square_col == selected_piece_col + 1
        ):
            for diagonal_col in [-1, 1]:
                capture_col = selected_piece_col + diagonal_col
                if (
                    not 0 <= capture_col < 8
                ):
                    possible_passant = False
                elif (
                    board[selected_piece_row + direction][capture_col] is not None
                    and board[selected_piece_row + direction][capture_col][:5]
                    != player_color
                ):
                    self.valid_moves.append(
                        (selected_piece_row + direction, capture_col)
                    )
                elif (
                    0 <= capture_col < 8
                    and board[selected_piece_row + direction][capture_col] is None
                    and selected_piece_row == en_passant_row
                    and possible_passant
                ):
                    self.valid_moves.append(
                        (selected_piece_row + direction, possible_passant_col)
                    )
                    self.en_passant = True

    def _define_horizontal_vertical_moves(
        self,
        selected_piece: str,
        selected_piece_row: int,
        selected_piece_col: int,
        selected_square_row: int,
        selected_square_col: int,
        board: list,
        color_slice: slice,
        piece_slice: slice,
        is_horizontal: bool,
        is_vertical: bool,
    ) -> None:
        """The purpose of this function is to define all the valid horizontal and vertical moves, not valid for the
        king, only for rook and queen.

        Args:
            selected_piece (str): String with the name of the selected piece, ej: White Pawn
            selected_piece_row (int): Number with the current row
            selected_piece_col (int): number with the current col
            selected_square_row (int): number of the row to move
            selected_square_col (int): number of the col to move
            board (list): array of arrays of the current board state.
            color_slice (slice): slice object to access the color of the piece.
            piece_slice (slice): Slice object referencing the owner of the piece
            is_horizontal (bool): True if current move is a horizontal move.
            is_vertical (bool): True if current move is a vertical move
        """

        if is_horizontal:
            current_index = selected_piece_col
            target_index = selected_square_col
            fixed_index = selected_piece_row
        elif is_vertical:
            current_index = selected_piece_row
            target_index = selected_square_row
            fixed_index = selected_piece_col
        else:
            return

        direction = -1 if current_index > target_index else 1

        while current_index != target_index + direction:
            current_index += direction

            if not 0 <= current_index < 8:
                return
            
            elif is_horizontal:
                current_square = (fixed_index, current_index)
                piece_at_square = board[fixed_index][current_index]
            elif is_vertical:
                current_square = (current_index, fixed_index)
                piece_at_square = board[current_index][fixed_index]
            else:
                return

            if piece_at_square is None:
                self.valid_moves.append(current_square)
                if selected_piece[piece_slice] == "King":
                    return
            elif piece_at_square[color_slice] == selected_piece[color_slice]:
                break
            elif piece_at_square[color_slice] != selected_piece[color_slice]:
                self.valid_moves.append(current_square)
                return

    def _define_diagonal_moves(
        self,
        selected_piece: str,
        selected_piece_row: int,
        selected_piece_col: int,
        selected_square_row: int,
        selected_square_col: int,
        board: list,
        color_slice: slice,
        piece_slice: slice,
    ) -> None:
        """The purpose of this function is to define the diagonal moves, valid for both bishop and queen.

        Args:
            selected_piece (str): Contains the name of the piece, ej. "White Bishop"
            selected_piece_row (int): Contains the row of the selected piece
            selected_piece_col (int): Contains the col of the selected piece
            selected_square_row (int): Contains the row of the selected square to move.
            selected_square_col (int): Contains the col of the selected square to move.
            board (list): Array of arrays with the state of the board.
            color_slice (slice): Slice object to access the color of the piece.
            piece_slice (slice): Slice object referencing the owner of the piece
        """
        current_row, current_col = selected_piece_row, selected_piece_col

        if (
            selected_square_row > selected_piece_row
            and selected_square_col > selected_piece_col
        ):
            direction_row, direction_col = 1, 1
        elif (
            selected_square_row > selected_piece_row
            and selected_square_col < selected_piece_col
        ):
            direction_row, direction_col = 1, -1
        elif (
            selected_square_row < selected_piece_row
            and selected_square_col < selected_piece_col
        ):
            direction_row, direction_col = -1, -1
        elif (
            selected_square_row < selected_piece_row
            and selected_square_col > selected_piece_col
        ):
            direction_row, direction_col = -1, 1
        else:
            return

        while (
            current_row != selected_square_row + direction_row
            and current_col != selected_square_col + direction_col
        ):
            current_row += direction_row
            current_col += direction_col

            if not 0 <= current_row < 8 or not 0 <= current_col < 8:
                return
            
            piece_at_square = board[current_row][current_col]
            
            if board[current_row][current_col] is None:
                self.valid_moves.append((current_row, current_col))
                if selected_piece[piece_slice] == "King":
                    return
            elif (
                board[current_row][current_col][color_slice]
                == selected_piece[color_slice]
            ):
                return
            elif piece_at_square[color_slice] != selected_piece[color_slice]:
                self.valid_moves.append((current_row, current_col))
                return

    def _define_knight_moves(
        self,
        selected_piece: str,
        selected_piece_row: int,
        selected_piece_col: int,
        board: list,
        color_slice: slice,
    ) -> None:
        """The purpose of this function is to define the valid moves for the knight.

        Args:
            selected_piece (str): Name of the piece ej. "White Knight"
            selected_piece_row (int): row of the selected piece.
            selected_piece_col (int): col of the selected piece.
            board (list): Array of arrays with the current state of the board.
            color_slice (slice): Slice object valid to access the color of the string piece.
        """
        for row in [-2, -1, 1, 2]:
            for col in [-2, -1, 1, 2]:
                current_row = selected_piece_row + row
                current_col = selected_piece_col + col
                if not 0 <= current_row < 8 or not 0 <= current_col < 8:
                    continue
                elif abs(row) == abs(col):
                    continue
                elif board[current_row][current_col] is None:
                    self.valid_moves.append((current_row, current_col))
                elif (
                    board[current_row][current_col][color_slice]
                    == selected_piece[color_slice]
                ):
                    continue
                else:
                    self.valid_moves.append((current_row, current_col))

    def _castle(
        self,
        selected_piece: str,
        selected_piece_row: int,
        selected_piece_col: int,
        selected_square_col: int,
        board: list,
        color_slice: slice,
        piece_slice: slice,
    ):
        """The purpose of this function is to castle.

        Args:
            selected_piece (str): String with the selected piece
            selected_piece_row (int): integer with the selected piece row
            selected_piece_col (int): integer with the selected piece col
            selected_square_col (int): selected square col int
            board (list): array of arrays with the current state of the board.
            color_slice (slice): Slice object to access the color of the piece.
            piece_slice (slice): Slice object to access the name of the piece
        """
        if selected_piece_col < selected_square_col:
            squares_move = 2
            rook_pos = 3
            rook_direction = -1
            king_direction = 2
            iter_direction = 1
            castle_dir = "Short"
        else:
            squares_move = 3
            rook_pos = -4
            rook_direction = 1
            king_direction = -2
            iter_direction = -1
            castle_dir = "Long"

        if selected_piece[color_slice] == "White":
            starting_row = 7
        else:
            starting_row = 0

        if selected_piece_row == starting_row:
            if (
                selected_piece_col + king_direction == selected_square_col
                and board[selected_piece_row][selected_piece_col + rook_pos][
                    piece_slice
                ]
                == "Rook"
            ):
                # The objective here is to iterate over the squares between the King and the Rook to see if they are
                # empty, utilizing the values defined above.
                for i in range(1, squares_move + iter_direction):
                    if (
                        board[selected_piece_row][
                            selected_piece_col + i * iter_direction
                        ]
                        is not None
                    ):
                        return
                self.valid_moves.append((selected_piece_row, selected_square_col))
                board[selected_piece_row][selected_piece_col + rook_pos] = None
                board[selected_piece_row][selected_square_col + rook_direction] = f"{selected_piece[color_slice]} Rook"
                self.castle = castle_dir

    def define_valid_moves(
        self,
        selected_piece: str,
        selected_piece_pos: tuple,
        selected_square: tuple,
        board: list,
        color_slice: slice,
        piece_slice: slice,
        possible_passant: bool,
        possible_passant_col: int,
        turn: str,
    ):
        """This is the function that will call the functions that contain the logic to move each piece.

        Args:
            selected_piece (str): selected_piece (str): a string containing the name of the piece ej. White pawn
            selected_piece_pos (tuple): a tuple containing the position on the board from the selected piece to move.
            selected_square (tuple): a tuple containing the position on the board of the selected square to move.
            board (List): array of arrays with the current state of the board.
            color_slice (slice): Contains a slice object that references the color of the piece string in format "White
            Pawn"
            piece_slice (slice): Contains a slice object that references the Piece of the piece string in format "White
            Pawn"
            possible_passant (bool): Bool that indicates if the en passant is possible in the next turn depending on the
            previous move
            possible_passant_col (int): The column in which the possible enpassant is located.
            turn (str): String with the current turn Black or White.
        """
        self.valid_moves.clear()
        selected_piece_row, selected_piece_col = selected_piece_pos
        selected_square_row, selected_square_col = selected_square
        is_horizontal = False
        is_vertical = False

        if selected_piece[color_slice] != turn:
            return

        if selected_piece_row == selected_square_row:
            is_horizontal = True
        elif selected_piece_col == selected_square_col:
            is_vertical = True

        if selected_piece[piece_slice] == "Pawn":
            self._define_pawn_moves(
                selected_piece,
                selected_piece_row,
                selected_piece_col,
                selected_square_col,
                board,
                color_slice,
                possible_passant,
                possible_passant_col,
            )
        elif selected_piece[piece_slice] == "Rook":
            self._define_horizontal_vertical_moves(
                selected_piece,
                selected_piece_row,
                selected_piece_col,
                selected_square_row,
                selected_square_col,
                board,
                color_slice,
                piece_slice,
                is_horizontal,
                is_vertical,
            )
        elif selected_piece[piece_slice] == "Knight":
            self._define_knight_moves(
                selected_piece,
                selected_piece_row,
                selected_piece_col,
                board,
                color_slice,
            )
        elif selected_piece[piece_slice] == "Bishop":
            self._define_diagonal_moves(
                selected_piece,
                selected_piece_row,
                selected_piece_col,
                selected_square_row,
                selected_square_col,
                board,
                color_slice,
                piece_slice,
            )
        elif (
            selected_piece[piece_slice] == "Queen"
            or selected_piece[piece_slice] == "King"
        ):
            self._define_horizontal_vertical_moves(
                selected_piece,
                selected_piece_row,
                selected_piece_col,
                selected_square_row,
                selected_square_col,
                board,
                color_slice,
                piece_slice,
                is_horizontal,
                is_vertical,
            )
            self._define_diagonal_moves(
                selected_piece,
                selected_piece_row,
                selected_piece_col,
                selected_square_row,
                selected_square_col,
                board,
                color_slice,
                piece_slice,
            )
        if selected_piece[piece_slice] == "King":
            self._castle(
                selected_piece,
                selected_piece_row,
                selected_piece_col,
                selected_square_col,
                board,
                color_slice,
                piece_slice,
            )

    def valid_move(self, selected_square: tuple) -> bool:
        """this functions checks if the selected square to move is contained within the list of valid moves, calls to
        execute the move_piece function on the movements.py

        Args:
            selected_square (tuple): tuple that contains the position on the board of the selected square.

        Returns:
            a boolean value stating if it is within the list of valid moves for the piece.
        """
        return selected_square in self.valid_moves
