import pygame
import COLORS as colors
from life_engine import Engine

class Button:
    def __init__(self, app, x_pos, y_pos, text_input):
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 45)
        self.app = app
        self.image = pygame.image.load("assets/buttons/button.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (400, 150))
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = self.font.render(self.text_input, False, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
    def update_image(self):
        self.app.screen.blit(self.image, self.rect)
        self.app.screen.blit(self.text, self.text_rect)
        
    def check_input(self, position_mouse):
        if position_mouse[0] in range(self.rect.left, self.rect.right) and position_mouse[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def change_color(self, position_mouse):
        if position_mouse[0] in range(self.rect.left, self.rect.right) and position_mouse[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, "Black")
        else:
            self.text = self.font.render(self.text_input, True, "White")


