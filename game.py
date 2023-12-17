import time
import pygame
from player import Player
from constants import WINNING_COLOR, COORDINATES_GAME_WIN, COORDINATES_GAME_LOSE, COORDINATES_GAME_DRAW, \
    COORDINATES_CONTINUE


class Game():
    def __init__(self):
        self.player_score = 0
        self.computer_score = 0
        self.round = True
        self.player = None
        self.winner = None
        self.font = pygame.font.Font(None, 36)
        self.field = {i: {'occupied': False, 'player': None, 'winning_row': False, 'winning_direction': None} for i in
                      range(1, 10)}
        self.winning_conditions = self.set_conditions()

    def set_conditions(self):
        winning_conditions = []
        for i in range(3):
            winning_conditions.append({'horizontal': [(3 * i + j) for j in range(1, 4)]})
        for i in range(3):
            winning_conditions.append({'vertical': [(i + j + 2 * (j - 1)) for j in range(1, 4)]})
        winning_conditions.append({'diagonal': [(j + (j - 1) * 3) for j in range(1, 4)]})
        winning_conditions.append({'diagonal': [(j + j + 1) for j in range(1, 4)]})
        return winning_conditions

    def game_player_round(self, field_number):
        if self.field[field_number]['occupied'] == False:
            if self.round == True:
                self.player = Player.PLAYER_X.value
                self.round = False
            else:
                self.player = Player.PLAYER_O.value
                self.round = True
                time.sleep(.5)
            self.field[field_number]['occupied'] = True
            self.field[field_number]['player'] = self.player

    # def process_player_move (self, field_number):
    #     if self.field[field_number]['occupied'] == False:
    #         self.round = False
    #         self.field[field_number]['occupied'] = True
    #         self.field[field_number]['player'] = self.player
    #         time.sleep(0.5)

    # def process_computer_move (self):
    #     None

    def win_round(self):
        for condition in self.winning_conditions:
            direction, indices = list(condition.items())[0]
            if all(self.field[index]['occupied'] and self.field[index]['player'] == self.player for index in indices):
                self.winner = self.player
                for index in indices:
                    self.field[index]['winning_row'] = True
                    self.field[index]['winning_direction'] = direction
                return True
        return False

    def draw(self):
        if all(self.field[index]['occupied'] == True and self.field[index]['winning_row'] == False for index in
               self.field):
            return True
        return False

    def display_winner(self, screen):
        if self.winner is not None:
            if self.winner == Player.PLAYER_X.value:
                text = 'Congratulations you won!'
                text_coordinates = COORDINATES_GAME_WIN
            elif self.winner == Player.PLAYER_O.value:
                text = 'You lost this round.'
                text_coordinates = COORDINATES_GAME_LOSE
        self.display_text(screen, text, text_coordinates)

    def display_draw(self, screen):
        text = 'DRAW!'
        self.display_text(screen, text, COORDINATES_GAME_DRAW)

    def display_text(self, screen, text, coordinates):
        display_text = self.font.render(text, True, WINNING_COLOR)
        screen.blit(display_text, coordinates)
        continue_text = self.font.render('Click to continue.', True, WINNING_COLOR)
        screen.blit(continue_text, COORDINATES_CONTINUE)
        pygame.display.flip()
        self.wait()
        self.reset_game()

    def wait(self):
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_click = False

    def reset_game(self):
        self.round = True
        self.player = None
        self.winner = None
        for key in self.field:
            self.field[key]['occupied'] = False
            self.field[key]['player'] = None
            self.field[key]['winning_row'] = False
            self.field[key]['winning_direction'] = False
