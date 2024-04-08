class Rules:
    def __init__(self) -> None:
        """intializes the list to pass as an argument on a function."""
        self.valid_moves = list()

    def _define_pawn_moves(
        self,
        selected_piece,
        selected_piece_row,
        selected_piece_col,
        selected_square_col,
        board,
    ):
        """This method is used to determine the valid moves for a given pawn, wether a capture or a move forward.

        Args:
            selected_piece (str): a tring containing the name of the piece ej. White pawn
            selected_piece_row (int): number of the row in which the piece currently is.
            selected_piece_col (int): number of the colmun in which the piece currently is.
            selected_square_col (int): column in which the selected square is (selected square to move)
            board (list): array of arrays.
        """
        if selected_piece[:5] == "White":
            player_color = "White"
            direction = -1
            start_row = 6
        else:
            player_color = "Black"
            direction = 1
            start_row = 1

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
                    and board[selected_piece_row + direction][capture_col]
                ):
                    if (
                        board[selected_piece_row + direction][capture_col][:5]
                        != player_color
                    ):
                        self.valid_moves.append(
                            (selected_piece_row + direction, capture_col)
                        )

    def define_valid_moves(
        self,
        selected_piece,
        selected_piece_pos,
        selected_square_owner,
        selected_square,
        board,
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

        if selected_piece[6:] == "Pawn":
            self._define_pawn_moves(
                selected_piece,
                selected_piece_row,
                selected_piece_col,
                selected_square_col,
                board,
            )

    def valid_move(self, selected_square):
        """this functions checks if the selected square to move is contained within the list of valid moves, calles to excetue the move_piece function on the movements.py

        Args:
            selected_square (tupple): tupple that contains the positon on the board of the selected square.

        Returns:
            a boolean value stating if it is within the list of valid moves.
        """
        return selected_square in self.valid_moves
