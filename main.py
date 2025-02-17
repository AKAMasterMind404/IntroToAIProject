import graph.graph as g
import pygame
import constants as cnt
import time

if __name__ == "__main__":
    pygame.init()

    screen_width, screen_height = 800, 800  # Default size
    cnt.CELL_SIZE, cnt.SCREEN_SIZE = cnt.update_grid_constants(cnt.GRID_SIZE, screen_width, screen_height)

    screen = pygame.display.set_mode(cnt.SCREEN_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("The Bot is on Fire!")

    graph = g.ManhattanGraph(screen, cnt.GRID_SIZE)
    graph.create_manhattan_graph()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                cnt.CELL_SIZE, cnt.SCREEN_SIZE = cnt.update_grid_constants(cnt.GRID_SIZE, screen_width, screen_height)
                screen = pygame.display.set_mode(cnt.SCREEN_SIZE, pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if cnt.SCREEN_SIZE[0] // 2 - 50 <= x <= cnt.SCREEN_SIZE[0] // 2 + 50 and cnt.SCREEN_SIZE[1] - 40 <= y <= \
                        cnt.SCREEN_SIZE[1] - 10:
                    if not graph.open_ship_initialized:
                        graph.initialize_ship_opening()
                    else:
                        if not graph.game_over:
                            while graph.step == 1:
                                graph.proceed()
                                time.sleep(0)
                            graph.proceed()

        g.draw_grid(screen, graph, cnt.GRID_SIZE)

    pygame.quit()