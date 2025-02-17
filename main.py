import pygame
import pygame_menu
import sys
from settings import WIDTH, HEIGHT, GAME_MODE
from table import Table
from button import Button

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")


class Pong:
    def __init__(self, screen):
        self.screen = screen
        self.FPS = pygame.time.Clock()

    def draw(self):
        pygame.display.flip()

    def main(self):
        my_theme = pygame_menu.themes.THEME_DARK.copy()
        my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE
        my_theme.widget_font = pygame_menu.font.FONT_8BIT
        mainmenu = pygame_menu.Menu(width=WIDTH,
                                    height=HEIGHT,
                                    title='Pong game',
                                    theme=my_theme)
        mainmenu.add.selector('Number of Players :',
                              [('1', 1), ('2', 2)], onchange=self.set_players)
        mainmenu.add.button('Play', self.game_loop)
        mainmenu.add.button('Quit', pygame_menu.events.EXIT)

        mainmenu.mainloop(screen)
        pygame.display.update()

    # Functions to start the game
    def set_players(self, value, players):
        GAME_MODE = players  # Update the game mode in settings

    def game_loop(self):
        table = Table(self.screen)  # pass to table the player_option saved to table.game_mode
        while True:
            self.screen.fill("black")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            table.player_move()
            table.update()
            self.draw()
            self.FPS.tick(30)


if __name__ == "__main__":
    pong_instance = Pong(screen)
    pong_instance.main()
