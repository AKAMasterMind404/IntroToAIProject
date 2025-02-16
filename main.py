import graph.graph as g
import pygame
import constants as cnt

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(cnt.SCREEN_SIZE)
    pygame.display.set_caption("The Bot is on Fire!")
    graph = g.ManhattanGraph(screen, 4)
    graph.create_manhattan_graph()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if cnt.SCREEN_SIZE[0] // 2 - 50 <= x <= cnt.SCREEN_SIZE[0] // 2 + 50 and cnt.SCREEN_SIZE[1] - 40 <= y <= \
                        cnt.SCREEN_SIZE[1] - 10:
                    if not graph.open_ship_initialized:
                        graph.initialize_ship_opening()
                    else:
                        graph.proceed()
    pygame.quit()
