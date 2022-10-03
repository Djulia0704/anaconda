import player
import my_game
import pygame
import time


class SnakeChain:
    def __init__(self, x, y, direction):
        self.position_x = x
        self.position_y = y
        self.direction = direction

        self.image = None
        self.update_image()
        self.rect = self.image.get_rect()

        self.next = None
        self.prev = None

    def update_image(self):
        pass

    def draw(self, screen):
        self.update_image()
        self.rect.x = self.position_x * my_game.GAME_FIELD_MIN_DIM
        self.rect.y = self.position_y * my_game.GAME_FIELD_MIN_DIM
        screen.blit(self.image, self.rect)


class SnakeHead (SnakeChain):
    def update_image(self):
        self.image = pygame.image.load("image/snake_head_{}.png".format(self.direction))


class SnakeBody (SnakeChain):
    def update_image(self):
        self.image = pygame.image.load("image/snake_body_{}.png".format(self.direction))


class Snake(player.Player):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.direction = "L"
        self.head = SnakeHead(x, y, self.direction)
        self.tail = None
        self.time = 0.0

    def check_direction(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and self.direction != "L":
                    self.direction = "R"
                if event.key == pygame.K_LEFT and self.direction != "R":
                    self.direction = "L"
                if event.key == pygame.K_UP and self.direction != "D":
                    self.direction = "U"
                elif event.key == pygame.K_DOWN and self.direction != "U":
                    self.direction = "D"

    def get_next_position(self):
        next_position_index_x = self.position_x
        next_position_index_y = self.position_y
        if self.direction == "R":
            next_position_index_x += 1
        elif self.direction == "L":
            next_position_index_x -= 1
        elif self.direction == "U":
            next_position_index_y -= 1
        elif self.direction == "D":
            next_position_index_y += 1
        return next_position_index_x, next_position_index_y

    def insert_new_body_chain(self):
        new_body_chain = SnakeBody(self.position_x, self.position_y, self.direction)
        next_body_chain = self.head.next
        self.head.next = new_body_chain
        new_body_chain.prev = self.head
        new_body_chain.next = next_body_chain
        if next_body_chain:
            next_body_chain.prev = new_body_chain

        if self.tail is None:
            self.tail = new_body_chain

    def update_position(self):
        self.game.set_symbol_at_index(self.head.position_x, self.head.position_y, "H")
        self.head.draw(self.game.get_screen())
        _next = self.head.next
        while _next:
            self.game.set_symbol_at_index(_next.position_x, _next.position_y, "B")
            _next.draw(self.game.get_screen())
            _next = _next.next

    def move(self):

        self.check_direction()

        if self.time == 0.0:
            self.time = time.time()
        else:
            time_now = time.time()

            if (time_now - self.time) >= 0.5:

                self.time = time_now

                next_position_index_x, next_position_index_y = self.get_next_position()

                next_position_symbol = self.game.get_symbol_at_index(next_position_index_x, next_position_index_y)

                if next_position_symbol == "W":
                    raise my_game.GameOverException()
                elif next_position_symbol == "B" and \
                        self.tail != self.game.get_player_at(next_position_index_x, next_position_index_y):
                    raise my_game.GameOverException()
                elif next_position_symbol == "R":

                    rabbit = self.game.get_player_at(next_position_index_x, next_position_index_y)
                    self.game.remove_player(rabbit)
                    self.game.set_symbol_at_index(next_position_index_x, next_position_index_y, "_")

                    self.insert_new_body_chain()
                    self.position_x = self.head.position_x = next_position_index_x
                    self.position_y = self.head.position_y = next_position_index_y
                    self.head.direction = self.direction

                else:

                    _next = self.head
                    while _next:
                        self.game.set_symbol_at_index(_next.position_x, _next.position_y, "_")
                        _next = _next.next

                    prev = self.tail
                    while prev:
                        if prev.prev:
                            prev.position_x = prev.prev.position_x
                            prev.position_y = prev.prev.position_y
                            prev.direction = prev.prev.direction
                        prev = prev.prev

                    self.position_x = self.head.position_x = next_position_index_x
                    self.position_y = self.head.position_y = next_position_index_y
                    self.head.direction = self.direction

        self.update_position()
