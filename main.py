import pygame
import configparser
from game import Game


class Main:
    def __init__(self, title):
        pygame.init()

        config = configparser.ConfigParser()
        config.read('config.ini')

        width = config.getint('DEFAULT', 'width', fallback=800)
        height = config.getint('DEFAULT', 'height', fallback=600)
        self.game = Game(width, height, title)

    def run(self):
        self.game.run()


if __name__ == "__main__":
    main = Main("Tower Defense")
    main.run()
