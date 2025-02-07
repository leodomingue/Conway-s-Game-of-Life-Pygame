import pygame
import COLORS as colors
from life_engine import Engine
from button import *
from options import Options
from simulation import Simulation


pygame.init()

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

        self.options = Options(self)
        self.simulation = Simulation(self)


    def run(self):
        # Runs the main menu loop

        menu = True
        while menu:
            self.screen.fill(colors.BLACK)
            MOUSE_POS = pygame.mouse.get_pos()

            # Create buttons with glowing border and text
            PLAY_BUTTON = Button(self, 400, 200, "Simulate", colors.GREEN, colors.WHITE)
            OPTIONS_BUTTON = Button(self, 400, 400, "Options", colors.GREEN, colors.WHITE)
            QUIT_BUTTON = Button(self, 400, 600, "Exit", colors.GREEN, colors.WHITE)

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
                            self.simulation.run_simulation()
                        if OPTIONS_BUTTON.check_input(MOUSE_POS):
                            self.options.options_game()
                        if QUIT_BUTTON.check_input(MOUSE_POS):
                            pygame.quit()
                            exit()
            

            pygame.display.update()
            self.clock.tick(self.FPS)

if __name__ == "__main__":
    app = App()
    app.run()