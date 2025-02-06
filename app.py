import pygame
import COLORS as colors
from life_engine import Engine
from typing import Tuple
import numpy as np
import bloom



pygame.init()

color_dict = {name: value for name, value in vars(colors).items() if isinstance(value, tuple)}
color_list = list(color_dict.values())

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
        """Changes text color when hovered."""
        self.is_hovered = self.rect.collidepoint(position_mouse)

    def handle_click(self):
        self.on_click()




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
        self.cell_size = 10

        self.live_cell_color = colors.WHITE
        self.dead_cell_color = colors.BLACK

        # Create an instance of the Grid class
        self.grid = Engine(self.WINDOW_WIDTH, self.WINDOW_HEIGHT - self.INTERFACE_HEIGHT,self.cell_size, self.INTERFACE_HEIGHT, self.live_cell_color, self.dead_cell_color)

        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 20)

    def create_interface(self):
        pygame.draw.rect(self.screen, colors.BLACK, (0, 0, self.WINDOW_WIDTH, self.INTERFACE_HEIGHT))

        text_input =  "Conway Game Life"
        text = self.font.render(text_input, False, "WHITE")
        text_rect = text.get_rect(center=(self.WINDOW_WIDTH//2, self.INTERFACE_HEIGHT//2))
        self.screen.blit(text, text_rect)

    def toggle_simulation(self):
        if self.grid.is_running():
            self.grid.stop()
            self.FPS = 60
        else:
            self.grid.start()
            self.FPS = 12

    def clear_simulation(self):
        self.grid.clear()
        if self.grid.is_running() == True:
            self.grid.start()
            self.grid.stop()
            self.FPS = 60

    def back_menu(self):
        self.FPS = 60
        self.grid.stop()
        self.clear_simulation()
        return False
    
    def nothing():
        print("a")

    def random_grid(self):
        self.grid.stop()
        self.grid.randomize()


    def run(self):
        """Runs the main menu loop."""
        menu = True
        while menu:
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

    def draw_palette(self, screen):
        color_dict = {name: value for name, value in vars(colors).items() if isinstance(value, tuple)}
        color_list = list(color_dict.values())
        for i, color in enumerate(color_list):
            pygame.draw.rect(screen, color, (10 + i * 50, 90, 40, 40))
            pygame.draw.rect(screen, color, (10 + i * 50, 500, 40, 40))

    def options_game(self):
        options_menu = True
        while options_menu:
            self.screen.fill((64, 64, 64))

            MOUSE_POS = pygame.mouse.get_pos()
            BACK_BUTTON = Button_Interface(self, 0, 0, "assets/back/back")

            self.draw_palette(self.screen)
            
            #Titles

            text_input_live =  "Live Cells Color: "
            text_live = self.font.render(text_input_live, False, "WHITE")
            text_rect_live = text_live.get_rect(topleft=(10, 60))
            self.screen.blit(text_live, text_rect_live)

            text_input_dead =  "Dead Cells Color: "
            text_dead = self.font.render(text_input_dead, False, "WHITE")
            text_rect_dead = text_dead.get_rect(topleft=(10, 470))
            self.screen.blit(text_dead, text_rect_dead)
            
            
            pygame.draw.rect(self.screen, self.live_cell_color, (text_rect_live.right-10,  text_rect_live.centery - 40 // 2-10, 40, 40))
            pygame.draw.rect(self.screen, self.dead_cell_color, (text_rect_dead.right-10,  text_rect_dead.centery - 40 // 2-10, 40, 40))

            for i, color in enumerate(color_list):
                            if 10 + i * 50 <= MOUSE_POS[0] <= 50 + i * 50 and 90 <= MOUSE_POS[1] <= 130:
                                pygame.draw.rect(self.screen, self.live_cell_color, (10 + i * 50, 90, 40, 40), 5)
                            if 10 + i * 50 <= MOUSE_POS[0] <= 50 + i * 50 and 500 <= MOUSE_POS[1] <= 540:
                                pygame.draw.rect(self.screen, self.dead_cell_color, (10 + i * 50, 500, 40, 40), 5)

            for button in [BACK_BUTTON]:
                button.change_color(MOUSE_POS)
                button.update_image()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit() 


                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MOUSE_POS[1] <50:
                        for button in [BACK_BUTTON]:
                            if button.rect.collidepoint(MOUSE_POS):
                                if button == BACK_BUTTON:
                                    options_menu = False
                    else:
                        for i, color in enumerate(color_list):
                            if 10 + i * 50 <= MOUSE_POS[0] <= 50 + i * 50 and 90 <= MOUSE_POS[1] <= 130:
                                self.live_cell_color = color
                                self.grid.set_live_cell_color(color)
                            if 10 + i * 50 <= MOUSE_POS[0] <= 50 + i * 50 and 500 <= MOUSE_POS[1] <= 540:
                                self.dead_cell_color = color
                                self.grid.set_dead_cell_color(color)


            pygame.display.update()
            self.clock.tick(self.FPS)


    def run_simulation(self):
        """Runs the Game of Life simulation."""
        simulation_running = True
        while simulation_running:
            self.screen.fill(colors.GRAY)
            self.create_interface()

            MOUSE_POS = pygame.mouse.get_pos()


            #Create buttons
            MORE_BUTTON = Button_Interface(self, 750, 0, "assets/more/more")
            RANDOM_BUTTON = Button_Interface(self, 650, 0, "assets/random/random", self.random_grid)
            BACK_BUTTON = Button_Interface(self, 0, 0, "assets/back/back", self.back_menu)
            CLEAR_BUTTON = Button_Interface(self, 100, 0, "assets/clear/clear", self.clear_simulation)


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
                        self.toggle_simulation()

                    if event.key == pygame.K_ESCAPE:
                        simulation_running = self.back_menu()

 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MOUSE_POS[1] <50:
                        for button in [MORE_BUTTON,RANDOM_BUTTON,BACK_BUTTON,CLEAR_BUTTON]:
                            if button.rect.collidepoint(MOUSE_POS):
                                if button == BACK_BUTTON:
                                    simulation_running = button.handle_click()
                                else:
                                    button.handle_click()
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