from grid import Grid
import COLORS as colors
import pygame
class Engine:
    def __init__(self, width, height, cell_size):
        self.grid = Grid(width,height,cell_size)
        self.cells_grid = self.grid.cells_grid
        self.rows = len(self.cells_grid)
        self.cols = len(self.cells_grid[0])
        self.cell_size = cell_size
        self.running = False

        self.temp_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
    def draw(self, window):
        self.grid.draw(window)

    def valid_position(self, position):
        if position[0] < 0 or position[0] >= self.rows or position[1] < 0 or position[1] >= self.cols:
            return False
        else:
            return True

    def count_live_cells_neighbors(self, row_pos, col_pos):
        total_neighbors = 0

        possible_neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]

        for neighbor in possible_neighbors:
            neighbor_pos = (row_pos + neighbor[0], col_pos + neighbor[1])
            if (self.valid_position(neighbor_pos) and self.cells_grid[neighbor_pos[0]][neighbor_pos[1]] ==1):
                total_neighbors += 1
        return total_neighbors
    
    def update(self):
        if self.is_running():
            """Update the grid based on the Game of Life rules."""
            for row in range(self.rows):
                for col in range(self.cols):
                    neighbors = self.count_live_cells_neighbors(row, col)
                    cell_value = self.cells_grid[row][col]

                    # Apply the Game of Life rules
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
            self.cells_grid, self.temp_grid = self.temp_grid, self.cells_grid

    def is_running(self):
        return self.running

    def start(self):
        self.running = True

    def stop(self):
        self.running = False

    def clear(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells_grid[row][col] = 0

    def handle_mouse_click(self, mouse_pos):
        col = mouse_pos[0] // self.cell_size
        row = mouse_pos[1] // self.cell_size

  
        if 0 <= row < self.rows and 0 <= col < self.cols:
            if self.cells_grid[row][col] == 1:
                self.cells_grid[row][col] = 0
            else:
                self.cells_grid[row][col] = 1

    def handle_mouse_no_click(self,window, mouse_pos):
        col = mouse_pos[0] // self.cell_size
        row = mouse_pos[1] // self.cell_size

        if 0 <= row < self.rows and 0 <= col < self.cols:
            pygame.draw.rect(window, colors.GRAY, (col* self.cell_size, row *self.cell_size, self.cell_size-1, self.cell_size-1))