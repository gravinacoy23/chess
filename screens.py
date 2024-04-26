import pygame
from button import Button


class Screen:
    def __init__(self) -> None:
        """initializes the core interface needs for the other classes"""
        self.screen = pygame.display.set_mode((1100, 780))
        pygame.display.set_caption("Chess")

        self.font_title = pygame.font.Font("media/font/font_bold.ttf", 200)
        self.font_subtitle = pygame.font.Font("media/font/font_bold.ttf", 100)
        self.font_text = pygame.font.Font("media/font/font_bold.ttf", 50)
        self.font_move_log = pygame.font.Font("media/font/font_bold.ttf", 30)

        self.background_color = pygame.Surface((1100, 780))
        self.background_color.fill("darkslategray1")
        self.screen.blit(self.background_color, (0, 0))


class MainMenuScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.chess_board_blur_surface = pygame.transform.scale(
            pygame.image.load("media/blur_elements/board_blur.png"), (700, 675)
        )
        self.chess_text = self.font_title.render("Chess", True, "White")
        self.local_button = Button(
            (435, 345), "Local", self.font_subtitle, "White", "Black"
        )
        self.bot_button = Button(
            (383, 510), "Bot", self.font_subtitle, "White", "Black"
        )
        self.settings_button = Button(
            (520, 675), "Settings", self.font_subtitle, "White", "Black"
        )

    def draw_main_menu(self):
        """The purpose of the function is to draw all the elements of the main menu, including the buttons for the
        other screen using the class Button"""
        self.screen.blit(self.chess_board_blur_surface, (197.5, 50))
        self.screen.blit(self.chess_text, (260, 50))
        self.local_button.update(self.screen)
        self.bot_button.update(self.screen)
        self.settings_button.update(self.screen)


class PlayScreen(Screen):

    def __init__(self) -> None:
        """Notice that this screen, since it's a child class from Screen, reassigns the value of self.chess_board_blur_surface to the image of the board without the blur.
        We also get the rect which will help us in our method.
        """
        super().__init__()
        self.white_time = 90 * 60
        self.black_time = 90 * 60
        self.chess_board_blur_surface = pygame.transform.scale(
            pygame.image.load("media/elements/board.png"), (700, 675)
        )
        self.chess_board_rect = self.chess_board_blur_surface.get_rect(
            topleft=(197.5, 50)
        )
        self.back_button = Button((60, 20), "Back", self.font_text, "Black", "White")
        self.background_clock_black = pygame.Surface((190, 60))
        self.background_clock_black.fill("White")
        self.background_clock_white = pygame.Surface((190, 60))
        self.background_clock_white.fill("White")

    def draw_play_screen(self):
        """The purpose of this function is to blit our main elements to the screen, without the pieces,
        only the board itself and the text/buttons."""
        self.screen.blit(self.background_color, (0, 0))
        self.screen.blit(self.chess_board_blur_surface, (197.5, 50))
        self.back_button.update(self.screen)

    def check_for_input(self, position: tuple) -> bool:
        """The purpose of this function is to check whether a position in specific is within the board, in this case,
        the position of the mouse.

        Args:
            position (Tuple): variable that's defined on the main file, at all times we are calculating the position of
            the mouse.

        Returns:
            Bool: The return statement is a boolean expression that says whether the mouse was on the screen on the last
             click event.
        """
        return position[0] in range(
            self.chess_board_rect.left, self.chess_board_rect.right
        ) and position[1] in range(
            self.chess_board_rect.top, self.chess_board_rect.bottom
        )

    def draw_clock(self, turn: str, clock) -> None:
        """The purpose of this function is to draw the clock on the play screen and count from 120 to zero as in
        classical chess. In the future we will have a setting for
        the clock to initialize form a different time.

        Args:
            turn (str): Defined on  the movements.py and passes as an argument on the main.py
            clock (Clock): Pygame data class, for the clock of the game.
        """
        if turn == "White":
            self.white_time -= clock.get_time() / 1000
            if self.white_time <= 0:
                self.white_time = 0
        if turn == "Black":
            self.black_time -= clock.get_time() / 1000
            if self.black_time <= 0:
                self.black_time = 0

        white_hours = int(self.white_time // 3600)
        white_minutes = int((self.white_time % 3600) // 60)
        white_seconds = int(self.white_time % 60)
        black_hours = int(self.black_time // 3600)
        black_minutes = int((self.black_time % 3600) // 60)
        black_seconds = int(self.black_time % 60)

        white_clock = self.font_text.render(
            f"{white_hours:02d}:{white_minutes:02d}:{white_seconds:02d}", True, "Black"
        )
        black_clock = self.font_text.render(
            f"{black_hours:02d}:{black_minutes:02d}:{black_seconds:02d}", True, "Black"
        )

        self.screen.blit(self.background_clock_black, (905, 310))
        self.screen.blit(self.background_clock_white, (905, 410))
        self.screen.blit(white_clock, (905, 410))
        self.screen.blit(black_clock, (905, 310))

    def draw_move_log(self, move_log_white: list, move_log_black: list) -> None:
        """This function takes care of drawing the move log on the screen

        Args:
            move_log_white (list): containing the move log for white
            move_log_black (list): containing the move log for black
        """
        for i, move in enumerate(move_log_white):
            move_text = self.font_move_log.render(move, True, "Black")
            self.screen.blit(move_text, (0, i * (50 + 5) + 50))
        for i, move in enumerate(move_log_black):
            move_text = self.font_move_log.render(move, True, "Black")
            self.screen.blit(move_text, (100, i * (50 + 5) + 50))


class BotScreen(PlayScreen):
    def __init__(self) -> None:
        """The only purpose of this subclass (so far) is to have a different screen for the Bot mode with the word
        Bot instead of Player 2."""
        super().__init__()


class SettingsScreen(Screen):
    def __init__(self) -> None:
        super().__init__()

        self.chess_board_blur_surface = pygame.transform.scale(
            pygame.image.load("media/blur_elements/board_blur.png"), (700, 675)
        )
        self.chess_text = self.font_title.render("Chess", True, "White")
        self.pieces_button = Button(
            (550, 500), "Select colors", self.font_subtitle, "White", "Black"
        )
        self.back_button = Button((60, 20), "Back", self.font_text, "Black", "White")

    def draw_settings_screen(self):
        """Same as the previous Draw functions, this one draws the settings screen, in the future this might
        transform into a new subclass, or new screen, because the settings that we'll have is to select a different
        color for the pieces, this will be after most of the work is done.
        """
        self.screen.blit(self.chess_board_blur_surface, (197.5, 50))
        self.screen.blit(self.chess_text, (260, 50))
        self.pieces_button.update(self.screen)
        self.back_button.update(self.screen)
