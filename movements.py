import pygame

class Movements:
    def __init__(self) -> None:
        self.selected_piece = None
        self.selected_piece_pos = None
        self.selected_square = None
        self.previous_pos = None
        self.turn = 'White'

    def select_piece(self, board, mouse_pos): 
        clicked_row, clicked_col = self._convert_mousepos_to_board(mouse_pos)
        if board[clicked_col][clicked_row] is not None: 
            self.selected_piece = board[clicked_col][clicked_row]
            self.selected_piece_pos = (clicked_col, clicked_row)

    def select_square(self, mouse_pos):
            clicked_row, clicked_col = self._convert_mousepos_to_board(mouse_pos)
            self.selected_square = (clicked_col, clicked_row)

    def _convert_mousepos_to_board(self, position): 
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
            case _ if 52 <= col < 135 :
                col = 0
            case _ if 135 <= col < 220 :
                col = 1
            case _ if 220 <= col < 304 :
                col = 2
            case _ if 304 <= col < 388 :
                col = 3
            case _ if 388 <= col < 473 :
                col = 4
            case _ if 473 <= col < 556 :
                col = 5
            case _ if 556 <= col < 640 :
                col = 6
            case _ if 640 <= col < 724 :
                col = 7

        return row,col
    
    def move_piece(self, board):
        if (self.turn == 'White' and self.selected_piece[0:5] == "White") or (self.turn == 'Black' and self.selected_piece[0:5] == "Black"):
            if self.selected_piece_pos != self.selected_square:
                row_init, col_init = self.selected_piece_pos
                row_to_move, col_to_move = self.selected_square
                board[row_to_move][col_to_move] = self.selected_piece
                board[row_init][col_init] = None
                self.selected_piece = None
                if self.turn == "White":
                    self.turn = "Black"
                else: 
                    self.turn = "White"
        