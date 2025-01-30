import COLORS as colors
import pygame

class Grid:
    def __init__(self, width, height, cell_size, interface_height):
        self.cell_size = cell_size # Size of each cell in the grid
        self.rows = height//cell_size # Number of rows based on height
        self.cols = width//cell_size # Number of cols based on width
        self.interface_height = interface_height

         # Representation of the grid as a 2D array
        self.cells_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def draw(self, window):
        # Loop through all columns and rows of the grid
        for i in range(self.rows):
            for j in range(self.cols):

                # Choose color based on the cell state
                if (self.cells_grid[i][j] == 0):
                    color = colors.BLACK
                else:
                    color = colors.WHITE

                # Draw the cell as a rectangle with a slight gap for grid lines
                pygame.draw.rect(window, color, (j* self.cell_size, i *self.cell_size+self.interface_height, self.cell_size-1, self.cell_size-1))