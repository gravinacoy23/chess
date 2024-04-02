import pygame


class Chess_board:
    def __init__(self) -> None:
        """initializes the images of all the pieces."""
        self.pawn_image_white = pygame.image.load(
            "media/elements/pieces/white/pawn.png"
        )
        self.rook_image_white = pygame.image.load(
            "media/elements/pieces/white/rook.png"
        )
        self.knight_image_white = pygame.image.load(
            "media/elements/pieces/white/knight.png"
        )
        self.bishop_image_white = pygame.image.load(
            "media/elements/pieces/white/bishop.png"
        )
        self.queen_image_white = pygame.image.load(
            "media/elements/pieces/white/queen.png"
        )
        self.king_image_white = pygame.image.load(
            "media/elements/pieces/white/king.png"
        )
        self.pawn_image_black = pygame.image.load(
            "media/elements/pieces/black/pawn.png"
        )
        self.rook_image_black = pygame.image.load(
            "media/elements/pieces/black/rook.png"
        )
        self.knight_image_black = pygame.image.load(
            "media/elements/pieces/black/knight.png"
        )
        self.bishop_image_black = pygame.image.load(
            "media/elements/pieces/black/bishop.png"
        )
        self.queen_image_black = pygame.image.load(
            "media/elements/pieces/black/queen.png"
        )
        self.king_image_black = pygame.image.load(
            "media/elements/pieces/black/king.png"
        )
        self.board_image = pygame.transform.scale(
            pygame.image.load("media/elements/board.png"), (700, 675)
        )

    def initalize_board(self, screen):
        """The purpose of this function is to initialize the matrix of the board with the pieces on their iniital position, taking care of
        both asigning the iniital position a bliting the image to the screen.

        Args:
            screen (Play_screen or Bot_screen): this argument is intended to be received on the main file and these are subclases from the file screeens.
        """
        self.board = [None] * 8
        for col in range(0, 8):
            self.board[col] = [None] * 8
        for row in range(0, 8):
            for col in range(0, 8):
                if row == 1:
                    self.board[row][col] = "Black Pawn"
                    piece_pos = (col * 87.5 + 210, row * 84.5 + 54)
                    screen.blit(self.pawn_image_black, piece_pos)
                elif row == 6:
                    self.board[row][col] = "White Pawn"
                    piece_pos = (col * 87.5 + 210, row * 84.5 + 54)
                    screen.blit(self.pawn_image_white, piece_pos)
                elif (col == 0 or col == 7) and (row == 0 or row == 7):
                    if row == 0:
                        self.board[row][col] = "Black Rook"
                        piece_pos = (col * 87.5 + 210, row * 84.5 + 54)
                        screen.blit(self.rook_image_black, piece_pos)
                    else:
                        self.board[row][col] = "White Rook"
                        piece_pos = (col * 87.5 + 210, row * 84.5 + 54)
                        screen.blit(self.rook_image_white, piece_pos)
                elif (col == 1 or col == 6) and (row == 0 or row == 7):
                    if row == 0:
                        self.board[row][col] = "Black Knight"
                        piece_pos = (col * 88 + 200, row * 84.5 + 54)
                        screen.blit(self.knight_image_black, piece_pos)
                    else:
                        self.board[row][col] = "White Knight"
                        piece_pos = (col * 88 + 200, row * 84.5 + 54)
                        screen.blit(self.knight_image_white, piece_pos)
                elif (col == 2 or col == 5) and (row == 0 or row == 7):
                    if row == 0:
                        self.board[row][col] = "Black Bishop"
                        piece_pos = (col * 86.8 + 201.3, row * 84 + 52)
                        screen.blit(self.bishop_image_black, piece_pos)
                    else:
                        self.board[row][col] = "White Bishop"
                        piece_pos = (col * 86.8 + 201.3, row * 84 + 52)
                        screen.blit(self.bishop_image_white, piece_pos)
                elif col == 3 and (row == 0 or row == 7):
                    if row == 0:
                        self.board[row][col] = "Black Queen"
                        piece_pos = (col * 86.5 + 200, row * 84.2 + 52)
                        screen.blit(self.queen_image_black, piece_pos)
                    else:
                        self.board[row][col] = "White Queen"
                        piece_pos = (col * 86.5 + 200, row * 84.2 + 52)
                        screen.blit(self.queen_image_white, piece_pos)
                elif col == 4 and (row == 0 or row == 7):
                    if row == 0:
                        self.board[row][col] = "Black King"
                        piece_pos = (col * 88 + 200, row * 84.2 + 52)
                        screen.blit(self.king_image_black, piece_pos)
                    else:
                        self.board[row][col] = "White King"
                        piece_pos = (col * 88 + 200, row * 84.2 + 52)
                        screen.blit(self.king_image_white, piece_pos)

    def update_board(self, screen):
        """_summary_
        The purpose of this function is to update the board depending on the current state of matrix (array of arrays) self.board.

        Args:
            screen (Play_screen or Bot_screen): this argument is intended to be received on the main file and these are subclases from the file screeens.
        """
        screen.blit(self.board_image, (197.5, 50))

        for row in range(0, 8):
            for col in range(0, 8):
                if self.board[row][col] == "Black Pawn":
                    screen.blit(
                        self.pawn_image_black, (col * 87.5 + 210, row * 84.5 + 54)
                    )
                elif self.board[row][col] == "White Pawn":
                    screen.blit(
                        self.pawn_image_white, (col * 87.5 + 210, row * 84.5 + 54)
                    )
                elif self.board[row][col] == "Black Rook":
                    screen.blit(
                        self.rook_image_black, (col * 87.5 + 210, row * 84.5 + 54)
                    )
                elif self.board[row][col] == "White Rook":
                    screen.blit(
                        self.rook_image_white, (col * 87.5 + 210, row * 84.5 + 54)
                    )
                elif self.board[row][col] == "Black Knight":
                    screen.blit(
                        self.knight_image_black, (col * 88 + 200, row * 84.5 + 54)
                    )
                elif self.board[row][col] == "White Knight":
                    screen.blit(
                        self.knight_image_white, (col * 88 + 200, row * 84.5 + 54)
                    )
                elif self.board[row][col] == "Black Bishop":
                    screen.blit(
                        self.bishop_image_black, (col * 86.8 + 201.3, row * 84 + 52)
                    )
                elif self.board[row][col] == "White Bishop":
                    screen.blit(
                        self.bishop_image_white, (col * 86.8 + 201.3, row * 84 + 52)
                    )
                elif self.board[row][col] == "Black Queen":
                    screen.blit(
                        self.queen_image_black, (col * 86.5 + 200, row * 84.2 + 52)
                    )
                elif self.board[row][col] == "White Queen":
                    screen.blit(
                        self.queen_image_white, (col * 86.5 + 200, row * 84.2 + 52)
                    )
                elif self.board[row][col] == "Black King":
                    screen.blit(
                        self.king_image_black, (col * 88 + 200, row * 84.2 + 52)
                    )
                elif self.board[row][col] == "White King":
                    screen.blit(
                        self.king_image_white, (col * 88 + 200, row * 84.2 + 52)
                    )
