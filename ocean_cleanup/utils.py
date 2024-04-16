import pygame

# button class
class Button:
    def __init__(self, x, y, width, height, text, color, font, font_color, font_size):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.font = font
        self.font_color = font_color
        self.font_size = font_size

        self.status = "inactive"

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        text = self.font.render(self.text, True, self.font_color)
        text_rect = text.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text, text_rect)

    def is_clicked(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False