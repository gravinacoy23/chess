class Button: 
    def __init__(self, position: tuple, text_input, font, base_color, hovering_color, image = None) -> None:
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

    def update(self, screen):
        if self.image is None: 
            screen.blit(self.text, self.text_rect)
        else: 
            screen.blit(self.image, self.rect)
    
    def check_for_input(self,position) -> bool:
        return position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom)
    
    def change_color(self, position, screen):
        if position[0] in range(self.text_rect.left, self.text_rect.right) and position[1] in range(self.text_rect.top, self.text_rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            screen.blit(self.text, self.text_rect)
        else: 
            self.text = self.font.render(self.text_input, True, self.base_color)
            screen.blit(self.text, self.text_rect)
