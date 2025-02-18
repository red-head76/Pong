import pygame
import time
import sys
from player import Player
from ball import Ball


class Table:
    def __init__(self, screen, settings):
        self.screen = screen
        self.game_over = False
        self.score_limit = 10
        self.winner = None
        self.settings = settings
        self._generate_world()

        # text info
        self.font = pygame.font.SysFont('Bauhaus 93', 60)
        self.color = pygame.Color("white")

    # create and add player to the screen
    def _generate_world(self):
        self.playerA = Player(0, self.settings.height // 2 - (self.settings.player_height // 2),
                              self.settings.player_width, self.settings.player_height)
        self.playerB = Player(self.settings.width - self.settings.player_width,
                              self.settings.height // 2 - (self.settings.player_height // 2),
                              self.settings.player_width, self.settings.player_height)
        self.ball = Ball(self.settings.width // 2,
                         self.settings.height // 2,
                         self.settings.ball_size,
                         self.settings)

    def _ball_hit(self):
        # if ball is not hit by a player and pass through table sides
        if self.ball.rect.left >= self.settings.width:
            self.playerA.score += 1
            self.ball.rect.x = self.settings.width // 2
            time.sleep(1)
        elif self.ball.rect.right <= 0:
            self.playerB.score += 1
            self.ball.rect.x = self.settings.width // 2
            time.sleep(1)

        # if ball land in the player
        if pygame.Rect.colliderect(self.ball.rect, self.playerA.rect):
            self.ball.direction = "right"
        if pygame.Rect.colliderect(self.ball.rect, self.playerB.rect):
            self.ball.direction = "left"

    def _bot_movement(self):
        if self.ball.direction == "left" and self.ball.rect.centery != self.playerA.rect.centery:
            if self.ball.rect.top <= self.playerA.rect.top:
                if self.playerA.rect.top > 0:
                    self.playerA.move_up()
            if self.ball.rect.bottom >= self.playerA.rect.bottom:
                if self.playerA.rect.bottom < self.settings.height:
                    self.playerA.move_bottom()

    def _player_movement(self, player, up, down):
        keys = pygame.key.get_pressed()

        if keys[up]:
            if player.rect.top > 0:
                player.move_up()
        if keys[down]:
            if player.rect.bottom < self.settings.height:
                player.move_bottom()

    def player_move(self):
        # If 1 player
        if self.settings.n_players == 1:
            self._bot_movement()
        elif self.settings.n_players == 2:
            self._player_movement(self.playerA, pygame.K_w, pygame.K_s)
        else:
            raise ValueError(f"No valid N_PLAYERS {self.settings.n_players}")
        self._player_movement(self.playerB, pygame.K_UP, pygame.K_DOWN)

    def _show_score(self):
        A_score, B_score = str(self.playerA.score), str(self.playerB.score)
        A_score = self.font.render(A_score, True, self.color)
        B_score = self.font.render(B_score, True, self.color)
        self.screen.blit(A_score, (self.settings.width // 4, 50))
        self.screen.blit(B_score, ((self.settings.width // 4) * 3, 50))

    def _game_end(self):
        if self.winner is not None:
            print(f"{self.winner} wins!!")
            pygame.quit()
            sys.exit()

    def update(self):
        self._show_score()

        self.playerA.update(self.screen)
        self.playerB.update(self.screen)

        self._ball_hit()

        if self.playerA.score == self.score_limit:
            self.winner = "Opponent"

        elif self.playerB.score == self.score_limit:
            self.winner = "You"

        self._game_end()
        self.ball.update(self.screen)
