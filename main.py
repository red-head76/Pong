import pygame
import pygame_menu
import sys
from table import Table
from settings import settings


class Pong:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong")

        self.settings = settings()
        screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        self.screen = screen
        self.FPS = pygame.time.Clock()

    def draw(self):
        pygame.display.flip()

    def main(self):
        my_theme = pygame_menu.themes.THEME_DARK.copy()
        my_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_UNDERLINE
        my_theme.widget_font = pygame_menu.font.FONT_8BIT
        mainmenu = pygame_menu.Menu(width=self.settings.width,
                                    height=self.settings.height,
                                    title='Pong game',
                                    theme=my_theme)
        mainmenu.add.selector('Number of Players :',
                              [('1', 1), ('2', 2)], onchange=self.set_players)
        mainmenu.add.button('Play', self.game_loop)
        mainmenu.add.button('Quit', pygame_menu.events.EXIT)

        mainmenu.mainloop(self.screen)
        pygame.display.update()

    # Functions to start the game
    def set_players(self, value, players):
        self.settings.n_players = players  # Update the game mode in settings

    def game_loop(self):
        table = Table(self.screen, self.settings)
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
    pong_instance = Pong()
    pong_instance.main()
