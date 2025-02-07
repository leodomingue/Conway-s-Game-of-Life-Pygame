import pygame
import COLORS as colors
from button import Button_Interface

class Options:
    """Handles the options menu for the Game of Life simulation"""
    def __init__(self, app):
        self.app = app
        self.color_dict = {name: value for name, value in vars(colors).items() if isinstance(value, tuple)}
        self.color_list = list(self.color_dict.values())

    def draw_palette(self):
        # Draws the color palette for live and dead cells on the screen
        for i, color in enumerate(self.color_list):
            pygame.draw.rect(self.app.screen, color, (10 + i * 50, 90, 40, 40))
            pygame.draw.rect(self.app.screen, color, (10 + i * 50, 500, 40, 40))

    def options_game(self):
        # Runs the options menu loop, allowing the user to customize colors and return to the main menu
        options_menu = True
        while options_menu:
            self.app.screen.fill((64, 64, 64))
            MOUSE_POS = pygame.mouse.get_pos()
            BACK_BUTTON = Button_Interface(self.app, 0, 0, "assets/back/back")

            self.draw_palette()

            # Titles
            text_live = self.app.font.render("Live Cells Color: ", False, "WHITE")
            text_dead = self.app.font.render("Dead Cells Color: ", False, "WHITE")
            text_rect_live = text_live.get_rect(topleft=(10, 60))
            text_rect_dead = text_dead.get_rect(topleft=(10, 470))

            self.app.screen.blit(text_live, text_rect_live)
            self.app.screen.blit(text_dead, text_rect_dead)

            pygame.draw.rect(self.app.screen, self.app.live_cell_color, (text_rect_live.right-10, text_rect_live.centery - 20, 40, 40))
            pygame.draw.rect(self.app.screen, self.app.dead_cell_color, (text_rect_dead.right-10, text_rect_dead.centery - 20, 40, 40))

            for i, color in enumerate(self.color_list):
                if 10 + i * 50 <= MOUSE_POS[0] <= 50 + i * 50 and 90 <= MOUSE_POS[1] <= 130:
                    pygame.draw.rect(self.app.screen, self.app.live_cell_color, (10 + i * 50, 90, 40, 40), 5)
                if 10 + i * 50 <= MOUSE_POS[0] <= 50 + i * 50 and 500 <= MOUSE_POS[1] <= 540:
                    pygame.draw.rect(self.app.screen, self.app.dead_cell_color, (10 + i * 50, 500, 40, 40), 5)

            for button in [BACK_BUTTON]:
                button.change_color(MOUSE_POS)
                button.update_image()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MOUSE_POS[1] < 50:
                        if BACK_BUTTON.rect.collidepoint(MOUSE_POS):
                            options_menu = False
                    else:
                        for i, color in enumerate(self.color_list):
                            if 10 + i * 50 <= MOUSE_POS[0] <= 50 + i * 50 and 90 <= MOUSE_POS[1] <= 130:
                                self.app.live_cell_color = color
                                self.app.grid.set_live_cell_color(color)
                            if 10 + i * 50 <= MOUSE_POS[0] <= 50 + i * 50 and 500 <= MOUSE_POS[1] <= 540:
                                self.app.dead_cell_color = color
                                self.app.grid.set_dead_cell_color(color)

            pygame.display.update()
            self.app.clock.tick(self.app.FPS)
