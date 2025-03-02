from game.ui_game import ui_game
from game.auto_game import auto_game
import constants as cnt

if __name__ == "__main__":
    graph = auto_game(q=cnt.FIRE_RESISTANCE_QUOTIENT)
    print(graph.isFireExtinguished)
    print(graph.isFireExtinguished)
