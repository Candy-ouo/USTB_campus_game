import sys
import os

sys.path.append(os.path.dirname(__file__))
from src.game import Game


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
