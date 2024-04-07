class Rules:
    def __init__(self) -> None:
        self.valid_moves = list()

    def define_valid_moves(self, selected_piece, selected_piece_pos, selected_square_owner, selected_square, board):
        selected_piece_row, selected_piece_col = selected_piece_pos
        selected_square_row, selected_square_col = selected_square

        if selected_piece[6:] == 'Pawn': 
            if selected_piece[:5] == 'White': 
                if board[selected_piece_row - 1][selected_piece_col] == None:
                    if selected_piece_row == 6: 
                        self.valid_moves.append(((selected_piece_row - 1), selected_piece_col))
                        self.valid_moves.append(((selected_piece_row - 2), selected_piece_col))
                    if selected_piece_col == 7: 
                        if board[selected_piece_row - 1][selected_piece_col - 1] != None:
                            self.valid_moves.append(((selected_piece_row - 1),(selected_piece_col - 1)))
                        return
                    if board[selected_piece_row - 1][selected_piece_col + 1] != None:
                        self.valid_moves.append(((selected_piece_row - 1),(selected_piece_col + 1)))
                    if board[selected_piece_row - 1][selected_piece_col - 1] != None:
                        self.valid_moves.append(((selected_piece_row - 1),(selected_piece_col - 1)))
                    else: 
                        self.valid_moves.append(((selected_piece_row - 1), selected_piece_col))
                else:
                    if board[selected_piece_row - 1][selected_piece_col + 1] != None:
                        self.valid_moves.append(((selected_piece_row - 1),(selected_piece_col + 1)))
                    if board[selected_piece_row - 1][selected_piece_col - 1] != None:
                        self.valid_moves.append(((selected_piece_row - 1),(selected_piece_col - 1)))
            elif selected_piece[:5] == 'Black':
                if board[selected_piece_row + 1][selected_piece_col] == None:
                    if selected_piece_row == 1: 
                        self.valid_moves.append(((selected_piece_row + 1), selected_piece_col))
                        self.valid_moves.append(((selected_piece_row + 2), selected_piece_col))
                    if selected_piece_col == 7: 
                        if board[selected_piece_row - 1][selected_piece_col - 1] != None:
                            self.valid_moves.append(((selected_piece_row - 1),(selected_piece_col - 1)))
                        return
                    if board[selected_piece_row + 1][selected_piece_col + 1] != None:
                        self.valid_moves.append(((selected_piece_row + 1),(selected_piece_col + 1)))
                    if board[selected_piece_row + 1][selected_piece_col - 1] != None:
                        self.valid_moves.append(((selected_piece_row + 1),(selected_piece_col - 1)))
                    else: 
                        self.valid_moves.append(((selected_piece_row + 1), selected_piece_col))
                else:
                    if board[selected_piece_row + 1][selected_piece_col + 1] != None:
                        self.valid_moves.append(((selected_piece_row + 1),(selected_piece_col + 1)))
                    if board[selected_piece_row + 1][selected_piece_col - 1] != None:
                        self.valid_moves.append(((selected_piece_row + 1),(selected_piece_col - 1)))

    def valid_move(self, selected_square): 
        return selected_square in self.valid_moves
    
"""
Loopfor the movements of bishops/queen to add several squares"""