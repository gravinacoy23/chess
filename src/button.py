class Button:
    def __init__(
        self, position: tuple, text_input, font, base_color, hovering_color, image=None
    ) -> None:
        """takes all the arguments for hte button to be initialized.

        Args:
            position (tuple): This is where we wanna blit the button
            text_input (string): This is what we want to display on the screen
            font (Font): Font type defined in the pygame library, serves to load whichever font I want to use, same for
            all the project in this case (with different sizes).
            base_color (string): color that we want the button to be when we are not hovering over it. Default color.
            hovering_color (string): Hovering color.
            image (Surface, optional): This is a type defined on the pygame Library. This parameter is in the case that
            we want to make an image a button. So far I haven't used this button, might be removed in the future among
            with the logic use for this. Defaults to None.
        """
        self.image = image
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if image is not None:
            self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen) -> None:
        """This method is to blit the button on the screen. It is necessary because if we call the blit method on the
        button after creating it won't work.

        Args: screen (Screen): this Could be type Screen or any of its subclasses, is the screen defined for each of
        the screens of the game.
        """
        if self.image is None:
            screen.blit(self.text, self.text_rect)
        else:
            screen.blit(self.image, self.rect)

    def check_for_input(self, position) -> bool:
        """Checks if we are hovering over the button, serves both to check if we clicked it and to change it's color
        when hovering.

        Args:
            position (Tuple): Mouse position defined on the main file.

        Returns:
            bool: Returns whether we are hovering over the button on a given position.
        """
        return position[0] in range(
            self.text_rect.left, self.text_rect.right
        ) and position[1] in range(self.text_rect.top, self.text_rect.bottom)

    def change_color(self, position, screen) -> None:
        """This is the function that takes care of changing the color of the button, and changes it back to the default
        color.

        Args:
            position (Tuple): Again, mouse position defined on main.py
            screen (Screen): Type defined on the screen.py
        """
        if self.check_for_input(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            screen.blit(self.text, self.text_rect)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
            screen.blit(self.text, self.text_rect)
