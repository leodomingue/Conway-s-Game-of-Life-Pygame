import pygame
import COLORS as colors
from life_engine import Engine


pygame.init()

class Button:
    """Represents a button with text that changes color when hovered."""

    def __init__(self, app, x_pos, y_pos, text_input):
        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 35)
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
        """Draws the button and its text on the screen."""
        self.app.screen.blit(self.image, self.rect)
        self.app.screen.blit(self.text, self.text_rect)
        
    def check_input(self, position_mouse):
        """Checks if the mouse is hovering over the button."""
        if position_mouse[0] in range(self.rect.left, self.rect.right) and position_mouse[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def change_color(self, position_mouse):
        """Changes text color when hovered."""
        if position_mouse[0] in range(self.rect.left, self.rect.right) and position_mouse[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, "Black")
        else:
            self.text = self.font.render(self.text_input, True, "White")







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



    def run(self):
        """Runs the main menu loop."""
        while True:
            self.screen.fill(colors.BLACK)
            MOUSE_POS = pygame.mouse.get_pos()

            # Create buttons
            PLAY_BUTTON = Button(self, 400, 200, "Simulate")
            OPTIONS_BUTTON = Button(self, 400, 400, "Optiones")
            QUIT_BUTTON = Button(self, 400, 600, "Exit")

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



    def run_simulation(self):
        """Runs the Game of Life simulation."""
        while True:
            self.screen.fill(colors.GRAY)

            MOUSE_POS = pygame.mouse.get_pos()
            
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
                            self.FPS = 10
                    if event.key == pygame.K_ESCAPE:
                        self.grid.clear()
                        if self.grid.is_running() == False:
                            self.grid.start()
                            self.grid.stop()

                if event.type == pygame.MOUSEBUTTONDOWN:
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