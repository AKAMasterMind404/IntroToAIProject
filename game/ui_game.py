import graph.graph as g
import pygame
import constants as cnt
import time
from helpers.draw_grid import draw_grid

def ui_game(graph):
    pygame.init()

    screen_width, screen_height = 800, 800  # Default size
    cnt.CELL_SIZE, cnt.SCREEN_SIZE = cnt.update_grid_constants(cnt.GRID_SIZE, screen_width, screen_height)

    screen = pygame.display.set_mode(cnt.SCREEN_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("The Bot is on Fire!")

    graph = g.ManhattanGraph(screen, cnt.GRID_SIZE)
    graph.create_manhattan_graph()