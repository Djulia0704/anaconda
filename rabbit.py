import random

import player
import pygame
import my_game
import time


class Rabbit(player.Player):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = pygame.image.load("image/rabbit2.png")
        self.rect = self.image.get_rect()
        self.time = 0.0

    def get_possible_moves(self):
        candidates = [(-1, -1), (0, -1), (1, -1),
                      (-1, 0),            (1, 0),
                      (-1, -1), (0, -1), (1, -1)]

        def check_candidate(candidate_) -> bool:
            return "_" == self.game.get_symbol_at_index(self.position_x + candidate_[0],
                                                        self.position_y + candidate_[1])
        result = []
        for candidate in candidates:
            if check_candidate(candidate):
                result.append(candidate)

        return result

    def move(self):

        if self.time == 0.0:
            self.time = time.time()
        else:
            time_now = time.time()

            if (time_now - self.time) >= 2.0:

                self.time = time_now

                to_move_or_not_to_move = random.randint(0, 1)
                if to_move_or_not_to_move:

                    possible_moves = self.get_possible_moves()
                    if len(possible_moves) > 0:

                        self.game.set_symbol_at_index(self.position_x, self.position_y, "_")

                        move_to_move = possible_moves[random.randint(0, len(possible_moves) - 1)]
                        self.position_x += move_to_move[0]
                        self.position_y += move_to_move[1]

                        self.game.set_symbol_at_index(self.position_x, self.position_y, "R")

        self.rect.x = self.position_x * my_game.GAME_FIELD_MIN_DIM
        self.rect.y = self.position_y * my_game.GAME_FIELD_MIN_DIM
        self.game.get_screen().blit(self.image, self.rect)
