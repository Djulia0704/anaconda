import pygame
import sys
import wall
import rabbit
import snake

GAME_FIELD_MIN_DIM = 50


class Game:
    def _parse_game_map(self, game_map_path) -> list:
        result = []
        with open(game_map_path, "r") as file:
            for line in file:
                line = line.strip("\n")
                result.append(line.split(" "))
        return result

    def __init__(self, game_map_path):
        self.game_field = self._parse_game_map(game_map_path)
        self.players = []

        self.screen = None
        self.bg_color = (0, 220, 0)

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode((GAME_FIELD_MIN_DIM * len(self.game_field[0]),
                                              GAME_FIELD_MIN_DIM * len(self.game_field)))
        pygame.display.set_caption("ANACONDA")

        for y in range(0, len(self.game_field)):
            for x in range(0, len(self.game_field[y])):
                symbol = self.get_symbol_at_index(x, y)
                if symbol == "W":
                    player = wall.Wall(self, x, y)
                    self.add_player(player)
                elif symbol == "R":
                    player = rabbit.Rabbit(self, x, y)
                    self.add_player(player)
                elif symbol == "S" or symbol == "H":
                    player = snake.Snake(self, x, y)
                    self.add_player(player)

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill(self.bg_color)

            for player in self.players:
                player.move()

            pygame.display.flip()

            # TODO підраховувати кроликів і якщо всі з'їдені переходимо на наступний рівень

    def get_screen(self):
        return self.screen

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_player_at(self, x, y):
        result = None
        for player in self.players:
            if player.position_x == x and player.position_y == y:
                result = player
        return result

        # відмічаємо на мапі
    def set_symbol_at_index(self, x, y, symbol):
        self.game_field[y][x] = symbol

    def get_symbol_at_index(self, x, y):
        return self.game_field[y][x]
