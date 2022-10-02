import player
import pygame
import my_game


class Wall(player.Player):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.image = pygame.image.load("image/wall.jpg")
        self.rect = self.image.get_rect()

    def move(self):
        self.rect.x = self.position_x * my_game.GAME_FIELD_MIN_DIM
        self.rect.y = self.position_y * my_game.GAME_FIELD_MIN_DIM
        self.game.get_screen().blit(self.image, self.rect)

