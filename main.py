import my_game


if __name__ == '__main__':
    game = my_game.Game("level/level1")
    try:
        game.run()
    except my_game.LevelDoneException:
        print("Level Done!")
    except my_game.GameOverException:
        print("Game Over!")
