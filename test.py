def _castle(
    self,
    selected_piece: str,
    selected_piece_row: int,
    selected_piece_col: int,
    selected_square_row: int,
    selected_square_col: int,
    board: list,
    color_slice: slice,
    piece_slice: slice,
    turn: str,
):
    if selected_piece_col > selected_square_col:
        squares_move = 2
        rook_pos = 3
        rook_direction = -1
        king_direction = 2
        iter_direction = 1
    else:
        squares_move = 3
        rook_pos = -4
        rook_direction = 1
        king_direction = -2
        iter_direction = 1

    if selected_piece[color_slice] == "White":
        starting_row = 7
    else:
        starting_row = 0

    if selected_piece_row == starting_row:
        if (
            selected_piece_col + king_direction == selected_square_col
            and board[selected_piece_row][selected_piece_col + rook_pos][piece_slice]
            == "Rook"
        ):
            for i in range(1, squares_move + 1):
                if (
                    board[selected_piece_row][selected_piece_col + i * iter_direction]
                    != None
                ):
                    return
            self.valid_moves.append((selected_piece_row, selected_square_col))
            board[selected_piece_row][selected_piece_col + rook_pos] = None
            board[selected_piece_row][
                selected_piece_col + rook_direction
            ] = f"{selected_piece[color_slice]} Rook"
