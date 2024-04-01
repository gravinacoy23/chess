import pygame
from button import Button
from board import Chess_board

class Screen: 
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((1100,780))
        pygame.display.set_caption('Chess')

        self.font_title = pygame.font.Font('media/font/font_bold.ttf', 200)
        self.font_subtitle = pygame.font.Font('media/font/font_bold.ttf', 100)
        self.font_text = pygame.font.Font('media/font/font_bold.ttf', 50)

        self.background_color = pygame.Surface((1100,780))
        self.background_color.fill("darkslategray1")
        self.screen.blit(self.background_color,(0,0))

class Main_menu_screen(Screen):
    def __init__(self) -> None:
        super().__init__()
        
        self.chess_board_blur_surface = pygame.transform.scale(pygame.image.load('media/blur_elements/board_blur.png'), (700,675))
        self.chess_text = self.font_title.render('Chess', True, "White")
        self.local_button = Button((435, 345), 'Local', self.font_subtitle, "White", "Black")
        self.bot_button = Button((383, 510), 'Bot', self.font_subtitle, "White", "Black")
        self.settings_button = Button((520, 675), 'Settings', self.font_subtitle, "White", "Black")

    def draw_main_menu(self):
        self.screen.blit(self.chess_board_blur_surface, (197.5,50)) 
        self.screen.blit(self.chess_text, (260, 50))
        self.local_button.update(self.screen)
        self.bot_button.update(self.screen)
        self.settings_button.update(self.screen)

class Play_screen(Screen):
    virtual_board = Chess_board()
    def __init__(self) -> None:
        super().__init__()
        self.chess_board_blur_surface = pygame.transform.scale(pygame.image.load('media/elements/board.png'), (700,675))
        self.chess_board_rect = self.chess_board_blur_surface.get_rect(topleft=(197.5, 50))
        self.player1_text = self.font_text.render('Player 1:', True, "Black")
        self.player2_text = self.font_text.render('Player 2:', True, "Black")
        self.back_button = Button((60,20), 'Back', self.font_text, 'Black', 'White')

    def draw_play_screen(self):
        self.screen.blit(self.background_color,(0,0))
        self.screen.blit(self.chess_board_blur_surface, (197.5,50)) 
        self.screen.blit(self.player2_text, (195, -7))
        self.screen.blit(self.player1_text, (195, 715))
        self.back_button.update(self.screen)
    
    def check_for_input(self, position): 
        return position[0] in range(self.chess_board_rect.left, self.chess_board_rect.right) and position[1] in range(self.chess_board_rect.top, self.chess_board_rect.bottom)

class Bot_screen(Play_screen):
    def __init__(self) -> None:
        super().__init__()
        self.player2_text = self.font_text.render('Bot', True, "Black")

class Settings_screen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.chess_board_blur_surface = pygame.transform.scale(pygame.image.load('media/blur_elements/board_blur.png'), (700,675))
        self.chess_text = self.font_title.render('Chess', True, "White")
        self.pieces_button = Button((550,500), 'Select colors', self.font_subtitle, 'White', 'Black')
        self.back_button = Button((60,20), 'Back', self.font_text, 'Black', 'White')

    def draw_settings_screen(self):
        self.screen.blit(self.chess_board_blur_surface, (197.5,50)) 
        self.screen.blit(self.chess_text, (260, 50))
        self.pieces_button.update(self.screen)
        self.back_button.update(self.screen)