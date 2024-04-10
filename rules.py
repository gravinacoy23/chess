class Rules:
    def __init__(self) -> None:
        """intializes the list to pass as an argument on a function."""
        self.valid_moves = list()
        self.en_passant = False

    def _define_pawn_moves(
        self,
        selected_piece,
        selected_piece_row,
        selected_piece_col,
        selected_square_col,
        board,
        color_slice, 
        possible_passant,
        possible_passant_col
    ):
        """This method is used to determine the valid moves for a given pawn, wether a capture or a move forward.

        Args:
            selected_piece (str): a tring containing the name of the piece ej. White pawn
            selected_piece_row (int): number of the row in which the piece currently is.
            selected_piece_col (int): number of the colmun in which the piece currently is.
            selected_square_col (int): column in which the selected square is (selected square to move)
            board (list): array of arrays.
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
                    0 <= capture_col < 8
                    and board[selected_piece_row + direction][capture_col] is not None
                ):
                    if (
                        board[selected_piece_row + direction][capture_col][:5]
                        != player_color
                    ):
                        self.valid_moves.append(
                            (selected_piece_row + direction, capture_col)
                        )
                        self.en_passant = False
                        possible_passant = False 
                        return
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
                    

    def define_valid_moves(
        self,
        selected_piece,
        selected_piece_pos,
        selected_square_owner,
        selected_square,
        board,
        color_slice,
        piece_sliece, 
        possible_passant,
        possible_passant_col
    ):
        """This is the function that will call the functions that contain the logic to move each piece.

        Args:
            selected_piece (str): selected_piece (str): a tring containing the name of the piece ej. White pawn
            selected_piece_pos (tupple): a tupple containing the position on the board from the selected piece to move.
            selected_square_owner (Str): A string containing the name of the owner of selected square to move.
            selected_square (tupple): a tupple containing the position on the board of the selected square to move.
            board (List): array of arrays with the current state of the board.
        """
        selected_piece_row, selected_piece_col = selected_piece_pos
        selected_square_row, selected_square_col = selected_square

        if selected_piece[piece_sliece] == "Pawn":
            self._define_pawn_moves(
                selected_piece,
                selected_piece_row,
                selected_piece_col,
                selected_square_col,
                board,
                color_slice, 
                possible_passant,
                possible_passant_col
            )

    def valid_move(self, selected_square):
        """this functions checks if the selected square to move is contained within the list of valid moves, calles to excetue the move_piece function on the movements.py

        Args:
            selected_square (tupple): tupple that contains the positon on the board of the selected square.

        Returns:
            a boolean value stating if it is within the list of valid moves.
        """
        return selected_square in self.valid_moves
