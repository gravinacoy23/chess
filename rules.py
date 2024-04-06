class Rules:
    def __init__(self) -> None:
        self.valid_moves = list()

    def define_valid_moves(self, selected_piece, selected_piece_pos, selected_square_owner, selected_square, board):
        selected_piece_row, selected_piece_col = selected_piece_pos
        selected_square_row, selected_square_col = selected_square

        if selected_piece[6:] == 'Pawn': 
            if selected_piece[:5] == 'White': 
                if selected_piece_row == 6: 
                    self.valid_moves.append(((selected_piece_row - 1), selected_piece_col))
                    self.valid_moves.append(((selected_piece_row - 2), selected_piece_col))
                else: 
                    self.valid_moves.append(((selected_piece_row - 1), selected_piece_col))
            elif selected_piece[:5] == 'Black':
                if selected_piece_row == 1: 
                    self.valid_moves.append(((selected_piece_row + 1), selected_piece_col))
                    self.valid_moves.append(((selected_piece_row + 2), selected_piece_col))
                else:
                    self.valid_moves.append(((selected_piece_row + 1), selected_piece_col))
                    
    def valid_move(self, selected_square): 
        return selected_square in self.valid_moves