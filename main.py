import pygame
from sys import exit

from button import Button
from screens import Main_menu_screen, Play_screen, Bot_screen, Settings_screen
from board import Chess_board
from movements import Movements


class Chess:
    def __init__(self) -> None:
        """initializes pygame and the clock"""
        pygame.init()
        self.clock = pygame.time.Clock()

    def _main_menu(self) -> None:
        """this functions is called at the begining of the game to initialize the GUI, uses the object of the screen file Main_menu_screen"""
        self.menu.screen.fill("black")
        self.menu.screen.fill("darkslategray1")
        while True:
            self.menu.draw_main_menu()
            mouse_pos = pygame.mouse.get_pos()
            # apply hovering effect and click action to all buttons

            for button in [
                self.menu.local_button,
                self.menu.bot_button,
                self.menu.settings_button,
            ]:
                button.change_color(mouse_pos, self.menu.screen)

            for event in pygame.event.get():
                # Event to close the game if the user clocks on the X button
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.menu.local_button.check_for_input(mouse_pos):
                        self._local_mode()
                    elif self.menu.bot_button.check_for_input(mouse_pos):
                        self._bot_mode()
                    elif self.menu.settings_button.check_for_input(mouse_pos):
                        self._settings_mode()

            # Draw all elements and update everything
            pygame.display.update()
            self.clock.tick(60)

    def _settings_mode(self) -> None:
        """initilizes setting screen, loops over buttons to apply effects."""
        self.menu.screen.fill("black")
        self.menu.screen.fill("darkslategray1")
        self.settings_screen.draw_settings_screen()
        while True:
            mouse_pos = pygame.mouse.get_pos()
            # apply hovering effect and click action to all buttons

            for button in [
                self.settings_screen.back_button,
                self.settings_screen.pieces_button,
            ]:
                button.change_color(mouse_pos, self.settings_screen.screen)

            for event in pygame.event.get():
                # Event to close the game if the user clocks on the X button
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.settings_screen.back_button.check_for_input(mouse_pos):
                        self._main_menu()

            # Draw all elements and update everything
            pygame.display.update()
            self.clock.tick(60)

    def _bot_mode(self) -> None:
        """Initialize the Bot screen, calling the method to draw the pieces and the board, no functionality to move pieces yet."""
        self.bot_screen.draw_play_screen()
        self.chess_board.initalize_board(self.bot_screen.screen)
        while True:
            self.bot_screen.draw_clock(self.movements.turn, self.clock)
            mouse_pos = pygame.mouse.get_pos()
            # apply hovering effect and click action to all buttons

            self.play_screen.back_button.change_color(
                mouse_pos, self.play_screen.screen
            )

            for event in pygame.event.get():
                # Event to close the game if the user clocks on the X button
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_screen.back_button.check_for_input(mouse_pos):
                        self._main_menu()

            # Draw all elements and update everything
            pygame.display.update()
            self.clock.tick(60)

    def _local_mode(self) -> None:
        """Has the ability to initilize board state and move the pieces, no rules to move pieces yet"""
        self.play_screen.draw_play_screen()
        self.chess_board.initialize_board(self.play_screen.screen)
        self.movements = Movements()
        self.movements.turn = "White"
        selecting_piece = True
        running = True
        while running:
            self.play_screen.draw_clock(self.movements.turn, self.clock)
            mouse_pos = pygame.mouse.get_pos()
            # apply hovering effect and click action to all buttons

            self.play_screen.back_button.change_color(
                mouse_pos, self.play_screen.screen
            )

            for event in pygame.event.get():
                # Event to close the game if the user clocks on the X button
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.bot_screen.back_button.check_for_input(mouse_pos):
                            self._main_menu()
                            running = False
                        elif self.play_screen.check_for_input(mouse_pos):
                            if selecting_piece:
                                self.movements.select_piece(
                                    self.chess_board.board, mouse_pos
                                )
                                if self.movements.selected_piece is not None:
                                    selecting_piece = False
                            else:
                                self.movements.select_square(
                                    self.chess_board.board, mouse_pos
                                )
                                if self.movements.selected_square is not None:
                                    self.movements.move_piece(
                                        self.chess_board.board, selecting_piece
                                    )
                                    self.chess_board.update_board(
                                        self.play_screen.screen
                                    )
                                    selecting_piece = True

            self.play_screen.draw_move_log(
                self.movements.move_log_white, self.movements.move_log_black
            )

            # Draw all elements and update everything
            pygame.display.update()
            self.clock.tick(60)

    def run_game(self) -> None:
        """Function that runs the game calling the main menu method and intializing objects to use throughout the program."""
        self.menu = Main_menu_screen()
        self.play_screen = Play_screen()
        self.bot_screen = Bot_screen()
        self.settings_screen = Settings_screen()
        self.chess_board = Chess_board()
        self._main_menu()


if __name__ == "__main__":
    chess_game = Chess()
    chess_game.run_game()
