import constants as cnt
import pygame

from game.ui_game import ui_game
from game.auto_game import auto_game
from graph.graph import GraphHelper

if __name__ == "__main__":
    screen_width, screen_height = 800, 800  # Default size
    cnt.CELL_SIZE, cnt.SCREEN_SIZE = cnt.update_grid_constants(cnt.GRID_SIZE, screen_width, screen_height)

    screen = pygame.display.set_mode(cnt.SCREEN_SIZE, pygame.RESIZABLE)
    graph = ui_game(screen, GraphHelper.openGraph)
