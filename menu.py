import pygame
import COLORS as colors
from life_engine import Engine


class App:
    def __init__(self):
        #dimensions
        self.WINDOW_WIDTH = 800
        self.WINDOW_HEIGHT = 800

        # Initialize the game window and clock
        self.screen =  pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        #frames
        self.FPS = 10

        # Grid cell size
        self.cell_size = 20

        # Create an instance of the Grid class
        self.grid = Engine(self.WINDOW_WIDTH, self.WINDOW_HEIGHT,self.cell_size)
        self.grid.cells_grid[1][8] = 1
        self.grid.cells_grid[1][9] = 1
        self.grid.cells_grid[1][10] = 1

        self.grid.cells_grid[2][8] = 1
        self.grid.cells_grid[2][10] = 1
        self.grid.cells_grid[3][8] = 1
        self.grid.cells_grid[3][9] = 1
        self.grid.cells_grid[3][10] = 1

        self.grid.cells_grid[2][9] = 1


    def run(self):
        # Main game loop
        while True:
            # Fill the screen with a background color
            self.screen.fill(colors.GRAY)
            
             # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.grid.update()

            # Draw the grid onto the screen
            self.grid.draw(self.screen)

            # Update the display and maintain the FPS
            pygame.display.update()
            self.clock.tick(self.FPS)
