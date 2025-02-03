import pygame
import COLORS as colors
from life_engine import Engine
from typing import Tuple
import numpy as np
import bloom



pygame.init()

class Button_Interface:
    """Represents a button """

    def __init__(self, app, x_pos, y_pos, image_path):
        self.app = app
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = pygame.image.load(f"{image_path}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.image_hover = pygame.image.load(f"{image_path}_hover.png").convert_alpha()
        self.image_hover = pygame.transform.scale(self.image_hover, (50, 40))
        self.rect = self.image.get_rect(topleft=(self.x_pos, self.y_pos))
        self.is_hovered = False


    def update_image(self):
        if self.is_hovered:
            self.app.screen.blit(self.image_hover, self.rect)
        else:
            self.app.screen.blit(self.image, self.rect)


    def change_color(self, position_mouse):
        """Changes text color when hovered."""
        self.is_hovered = self.rect.collidepoint(position_mouse)

    def handle_click(self, position_mouse):
        """Handles the button click event."""
        if self.rect.collidepoint(position_mouse): 
            print("a")





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
        """Draws the button with glowing border and text on the screen."""
        # Generate the glowing border
        border_image = bloom.glowing_border(self.image.copy(), 5,5,self.border_color)

        # Generate the glowing text
        text_image = bloom.glowing_text(self.image.copy(), self.text_input, self.text_color)

        # Combine the border and text images
        combined_image = np.bitwise_or(border_image, text_image)

        # Convert the numpy array to a pygame surface
        img_surface = pygame.surfarray.make_surface(np.fliplr(np.rot90(combined_image, k=-1)))

        self.app.screen.blit(img_surface, self.rect.topleft)

    def check_input(self, position_mouse):
        """Checks if the mouse is hovering over the button."""
        if self.rect.collidepoint(position_mouse):
            return True
        return False

    def change_color(self, position_mouse):
        """Changes text color when hovered."""
        if self.rect.collidepoint(position_mouse):
            self.text_color = colors.GREEN  
            self.border_color = colors.GREEN
        else:
            self.text_color = colors.WHITE 
            self.border_color = colors.WHITE







class App:
    """Main application that initializes the game and handles user interactions."""

    def __init__(self):
        #Window dimensions
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 810
        self.INTERFACE_HEIGHT = 50

        # Initialize the game window and clock
        self.screen =  pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        #Frames
        self.FPS = 60

        # Grid cell size
        self.cell_size = 20

        # Create an instance of the Grid class
        self.grid = Engine(self.WINDOW_WIDTH, self.WINDOW_HEIGHT - self.INTERFACE_HEIGHT,self.cell_size, self.INTERFACE_HEIGHT)

        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 20)

    def run(self):
        """Runs the main menu loop."""
        while True:
            self.screen.fill(colors.BLACK)
            MOUSE_POS = pygame.mouse.get_pos()

            # Create buttons with glowing border and text
            PLAY_BUTTON = Button(self, 400, 200, "Simulate", colors.YELLOW, colors.WHITE)
            OPTIONS_BUTTON = Button(self, 400, 400, "Options", colors.YELLOW, colors.WHITE)
            QUIT_BUTTON = Button(self, 400, 600, "Exit", colors.YELLOW, colors.WHITE)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.change_color(MOUSE_POS)
                button.update_image()

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                        if PLAY_BUTTON.check_input(MOUSE_POS):
                            self.run_simulation()
                        if OPTIONS_BUTTON.check_input(MOUSE_POS):
                            self.options_game()
                        if QUIT_BUTTON.check_input(MOUSE_POS):
                            pygame.quit()
                            exit()
            

            pygame.display.update()
            self.clock.tick(self.FPS)

    def create_interface(self):
        pygame.draw.rect(self.screen, colors.BLACK, (0, 0, self.WINDOW_WIDTH, self.INTERFACE_HEIGHT))

        text_input =  "Conway Game Life"
        text = self.font.render(text_input, False, "WHITE")
        text_rect = text.get_rect(center=(self.WINDOW_WIDTH//2, self.INTERFACE_HEIGHT//2))
        self.screen.blit(text, text_rect)



    def run_simulation(self):
        """Runs the Game of Life simulation."""
        while True:
            self.screen.fill(colors.GRAY)
            self.create_interface()

            MOUSE_POS = pygame.mouse.get_pos()


            #Create buttons
            MORE_BUTTON = Button_Interface(self, 750, 0, "assets/more/more")
            RANDOM_BUTTON = Button_Interface(self, 650, 0, "assets/random/random")
            BACK_BUTTON = Button_Interface(self, 0, 0, "assets/back/back")
            CLEAR_BUTTON = Button_Interface(self, 100, 0, "assets/clear/clear")


            for button in [MORE_BUTTON,RANDOM_BUTTON,BACK_BUTTON,CLEAR_BUTTON]:
                button.change_color(MOUSE_POS)
                button.update_image()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.grid.is_running():
                            self.grid.stop()
                            self.FPS = 60
                        else:
                            self.grid.start()
                            self.FPS = 12
                    if event.key == pygame.K_ESCAPE:
                        self.grid.clear()
                        if self.grid.is_running() == False:
                            self.grid.start()
                            self.grid.stop()
 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MOUSE_POS[1] <50:
                        for button in [MORE_BUTTON,RANDOM_BUTTON,BACK_BUTTON,CLEAR_BUTTON]:
                            button.handle_click(MOUSE_POS)
                    else:
                        adjusted_mouse_pos = (MOUSE_POS[0], MOUSE_POS[1] - self.INTERFACE_HEIGHT)
                        self.grid.handle_mouse_click(adjusted_mouse_pos)


            self.grid.update()

            # Draw the grid onto the screen
            self.grid.draw(self.screen)


            adjusted_mouse_pos = (MOUSE_POS[0], MOUSE_POS[1] - self.INTERFACE_HEIGHT)
            self.grid.handle_mouse_no_click(self.screen, adjusted_mouse_pos)

            # Update the display and maintain the FPS
            pygame.display.update()
            self.clock.tick(self.FPS)




if __name__ == "__main__":
    app = App()
    app.run()