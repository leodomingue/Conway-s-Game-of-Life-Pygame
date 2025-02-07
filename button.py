import pygame
import numpy as np
import bloom
import COLORS as colors

class Button:
    """Represents a button with glowing border and text."""

    def __init__(self, app, x_pos, y_pos, text_input, border_color, text_color):
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 35)
        self.app = app
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.text_input = text_input
        self.border_color = border_color
        self.text_color = text_color 

        # Create a base image for the button
        self.image = np.zeros((150, 400, 3), dtype=np.uint8)  
        self.rect = pygame.Rect(self.x_pos - 200, self.y_pos - 75, 400, 150)  

    def update_image(self):
        # Draws the button with glowing border and text on the screen
        # Generate the glowing border
        border_image = bloom.glowing_border(self.image.copy(), 5, 5, self.border_color)

        # Generate the glowing text
        text_image = bloom.glowing_text(self.image.copy(), self.text_input, self.text_color)

        # Combine the border and text images
        combined_image = np.bitwise_or(border_image, text_image)

        # Convert the numpy array to a pygame surface
        img_surface = pygame.surfarray.make_surface(np.fliplr(np.rot90(combined_image, k=-1)))

        self.app.screen.blit(img_surface, self.rect.topleft)

    def check_input(self, position_mouse):
        # Checks if the mouse is hovering over the button
        return self.rect.collidepoint(position_mouse)

    def change_color(self, position_mouse):
        # Changes text and border color when hovered
        if self.rect.collidepoint(position_mouse):
            self.text_color = colors.GREEN  
            self.border_color = colors.GREEN
        else:
            self.text_color = colors.WHITE 
            self.border_color = colors.WHITE

class Button_Interface:
    """Represents a button """

    def __init__(self, app, x_pos, y_pos, image_path, on_click=None):
        self.app = app
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.image.load(f"{image_path}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.image_hover = pygame.image.load(f"{image_path}_hover.png").convert_alpha()
        self.image_hover = pygame.transform.scale(self.image_hover, (50, 40))
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.is_hovered = False
        self.on_click = on_click


    def update_image(self):
        if self.is_hovered:
            self.app.screen.blit(self.image_hover, self.rect)
        else:
            self.app.screen.blit(self.image, self.rect)


    def change_color(self, position_mouse):
        # Changes text color when hovered
        self.is_hovered = self.rect.collidepoint(position_mouse)

    def handle_click(self):
        self.on_click()