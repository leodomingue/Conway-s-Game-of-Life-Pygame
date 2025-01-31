import COLORS as colors
import pygame

class Grid:
    # Initialize the grid
    def __init__(self, width, height, cell_size, interface_height):
        self.cell_size = cell_size 
        self.rows = height//cell_size 
        self.cols = width//cell_size 
        self.interface_height = interface_height

         
        self.cells_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def draw(self, window):
        # Draw the grid on the provided Pygame window
        for i in range(self.rows):
            for j in range(self.cols):

                
                if (self.cells_grid[i][j] == 0):
                    color = colors.BLACK
                else:
                    color = colors.WHITE

                
                pygame.draw.rect(window, color, (j* self.cell_size, i *self.cell_size+self.interface_height, self.cell_size-1, self.cell_size-1))