import pygame
import COLORS as colors
from button import Button_Interface


class Simulation:

    def __init__(self, app):
        self.app = app
        self.screen = app.screen
        self.clock = app.clock
        self.grid = app.grid
        self.INTERFACE_HEIGHT = app.INTERFACE_HEIGHT
        self.FPS = app.FPS

        self.font = pygame.font.Font("assets/font/PressStart2P-Regular.ttf", 20)

    def create_interface(self):
        #Creates title and black interface
        pygame.draw.rect(self.screen, colors.BLACK, (0, 0, self.app.WINDOW_WIDTH, self.INTERFACE_HEIGHT))
        text_input = "Conway Game Life"
        text = self.font.render(text_input, False, "WHITE")
        text_rect = text.get_rect(center=(self.app.WINDOW_WIDTH // 2, self.INTERFACE_HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def toggle_simulation(self):
        #Toggles the simulation between running and paused states
        if self.grid.is_running():
            self.grid.stop()
            self.FPS = 60
        else:
            self.grid.start()
            self.FPS = 12

    def clear_simulation(self):
        # Clears the grid and stops the simulation
        self.grid.clear()
        if self.grid.is_running():
            self.grid.start()
            self.grid.stop()
            self.FPS = 60

    def back_menu(self):
        # Returns to the main menu and stops the simulation
        self.FPS = 60
        self.grid.stop()
        self.clear_simulation()
        return False

    def random_grid(self):
        # Randomizes the grid and stops the simulation
        self.grid.stop()
        self.grid.randomize()



    def update_grid(self, MOUSE_POS):
        # Updates and draws the grid based on the current state
        self.grid.update()
        self.grid.draw(self.screen)

        adjusted_mouse_pos = (MOUSE_POS[0], MOUSE_POS[1] - self.INTERFACE_HEIGHT)
        self.grid.handle_mouse_no_click(self.screen, adjusted_mouse_pos)

    def run_simulation(self):
        # Runs the Game of Life simulation
        simulation_running = True
        while simulation_running:
            self.screen.fill(colors.GRAY)
            self.create_interface()

            MOUSE_POS = pygame.mouse.get_pos()

            MORE_BUTTON = Button_Interface(self.app, 750, 0, "assets/more/more")
            RANDOM_BUTTON = Button_Interface(self.app, 650, 0, "assets/random/random", self.random_grid)
            BACK_BUTTON = Button_Interface(self.app, 0, 0, "assets/back/back", self.back_menu)
            CLEAR_BUTTON = Button_Interface(self.app, 100, 0, "assets/clear/clear", self.clear_simulation)

            for button in [MORE_BUTTON, RANDOM_BUTTON, BACK_BUTTON, CLEAR_BUTTON]:
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
                    if MOUSE_POS[1] < 50:
                        for button in [MORE_BUTTON, RANDOM_BUTTON, BACK_BUTTON, CLEAR_BUTTON]:
                            if button.rect.collidepoint(MOUSE_POS):
                                if button == BACK_BUTTON:
                                    simulation_running = button.handle_click()
                                else:
                                    button.handle_click()
                    else:
                        adjusted_mouse_pos = (MOUSE_POS[0], MOUSE_POS[1] - self.INTERFACE_HEIGHT)
                        self.grid.handle_mouse_click(adjusted_mouse_pos)


            # Update and draw the grid
            self.update_grid(MOUSE_POS)

            # Update the display and maintain the FPS
            pygame.display.update()
            self.clock.tick(self.FPS)
