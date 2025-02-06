from grid import Grid
import COLORS as colors
import pygame
import random
class Engine:

    """This class handles the logic for Conway's Game of Life."""

    def __init__(self, width, height, cell_size, interface_height, live_cell_color, dead_cell_color):
        #Initializes the simulation engine.

        self.live_cell_color = live_cell_color
        self.dead_cell_color = dead_cell_color
        self.grid = Grid(width,height,cell_size, interface_height, self.live_cell_color, self.dead_cell_color)
        self.cells_grid = self.grid.cells_grid
        self.rows = len(self.cells_grid)
        self.cols = len(self.cells_grid[0])
        self.cell_size = cell_size
        self.running = False



        self.temp_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.interface_height = interface_height
        


    def set_live_cell_color(self, new_color):
        self.live_cell_color = new_color
        self.grid.set_live_cell_color(new_color) 

    def set_dead_cell_color(self, new_color):
        self.dead_cell_color = new_color
        self.grid.set_dead_cell_color(new_color) 
    
    def draw(self, window):
        #Draws the grid on the given window.
        self.grid.draw(window)

    def count_live_cells_neighbors(self, row, col):
        #Counts the number of live neighbors for a given cell
        live_neighbors = 0

        for i in range(-1, 2):
            for j in range(-1, 2):  
                if i == 0 and j == 0:
                    continue 

                
                neighbor_row = (row + i) % self.rows
                neighbor_col = (col + j) % self.cols

              
                live_neighbors += self.cells_grid[neighbor_row][neighbor_col]

        return live_neighbors
    
    def update(self):
        if self.is_running():

            #Updates the grid state according to Conway's Game of Life rules.
            for row in range(self.rows):
                for col in range(self.cols):
                    neighbors = self.count_live_cells_neighbors(row, col)
                    cell_value = self.cells_grid[row][col]

                    if cell_value == 1:
                        if neighbors < 2 or neighbors > 3:
                            self.temp_grid[row][col] = 0  # Cell dies
                        else:
                            self.temp_grid[row][col] = 1  # Cell survives
                    else:
                        if neighbors == 3:
                            self.temp_grid[row][col] = 1  # Cell is born
                        else:
                            self.temp_grid[row][col] = 0  # Cell stays dead

            # Swap the grids
            for row in range(self.rows):
                for col in range(self.cols):
                    self.cells_grid[row][col] = self.temp_grid[row][col]

    def is_running(self):
        #Checks if the simulation is currently running.
        return self.running

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def clear(self):
        #Clears the grid, setting all cells to dead (0).
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells_grid[row][col] = 0

    def handle_mouse_click(self, mouse_pos):
        # Handles user clicks on the grid, toggling the state of the clicked cell
        col = mouse_pos[0] // self.cell_size
        row = mouse_pos[1] // self.cell_size

  
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.cells_grid[row][col] == 1:
                self.cells_grid[row][col] = 0
            else:
                self.cells_grid[row][col] = 1

    def handle_mouse_no_click(self,window, mouse_pos):
        #Highlights the cell under the mouse pointer without clicking
        col = mouse_pos[0] // self.cell_size
        row = mouse_pos[1] // self.cell_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            pygame.draw.rect(window, colors.GRAY, (col* self.cell_size, row *self.cell_size+self.interface_height, self.cell_size-1, self.cell_size-1))

    def randomize(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells_grid[row][col] = random.choice([0, 1])