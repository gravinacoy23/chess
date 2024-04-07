class Rules:
    def __init__(self) -> None:
        self.valid_moves = list()

    def _define_pawn_moves(self, selected_piece, selected_piece_row, selected_piece_col, selected_square_col, board): 
        if selected_piece[:5] == 'White':
            player_color = 'White'
            direction = -1
            start_row = 6
        else:
            player_color = 'Black'
            direction = 1
            start_row = 1
        
        if board[selected_piece_row + direction][selected_piece_col] is None:
            self.valid_moves.append((selected_piece_row + direction, selected_piece_col))
            if selected_piece_row == start_row and board[selected_piece_row + 2*direction][selected_piece_col] is None: 
                self.valid_moves.append((selected_piece_row+2*direction, selected_piece_col))

        if selected_square_col == selected_piece_col - 1 or selected_square_col == selected_piece_col + 1:
            for diagonal_col in [-1,1]: 
                capture_col = selected_piece_col + diagonal_col
                if 0 <= capture_col < 8 and board[selected_piece_row + direction][capture_col]: 
                    if board[selected_piece_row + direction][capture_col][:5] != player_color: 
                        self.valid_moves.append((selected_piece_row+direction, capture_col))

    def define_valid_moves(self, selected_piece, selected_piece_pos, selected_square_owner, selected_square, board):
        selected_piece_row, selected_piece_col = selected_piece_pos
        selected_square_row, selected_square_col = selected_square

        if selected_piece[6:] == 'Pawn': 
            self._define_pawn_moves(selected_piece, selected_piece_row, selected_piece_col, selected_square_col, board)
        

    def valid_move(self, selected_square): 
        return selected_square in self.valid_moves
    
"""
Loopfor the movements of bishops/queen to add several squares"""