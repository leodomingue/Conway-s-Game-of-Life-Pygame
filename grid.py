import COLORS as colors
import pygame

class Grid:
    def __init__(self, width, height, cell_size):
        self.cell_size = cell_size # Size of each cell in the grid
        self.rows = height//cell_size # Number of rows based on height
        self.cols = width//cell_size # Number of cols based on width

         # Representation of the grid as a 2D array
        self.cells_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def draw(self, window):
        # Loop through all columns and rows of the grid
        for i in range(self.cols):
            for j in range(self.rows):

                # Choose color based on the cell state
                if (self.cells_grid[j][i] == 0):
                    color = colors.BLACK
                else:
                    color = colors.WHITE

                # Draw the cell as a rectangle with a slight gap for grid lines
                pygame.draw.rect(window, color, (i* self.cell_size, j *self.cell_size, self.cell_size-1, self.cell_size-1))