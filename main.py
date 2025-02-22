import graph.graph as g
import pygame
import constants as cnt
import time
from helpers.draw_grid import draw_grid

if __name__ == "__main__":
    pygame.init()

    screen_width, screen_height = 800, 800  # Default size
    cnt.CELL_SIZE, cnt.SCREEN_SIZE = cnt.update_grid_constants(cnt.GRID_SIZE, screen_width, screen_height)

    screen = pygame.display.set_mode(cnt.SCREEN_SIZE, pygame.RESIZABLE)
    pygame.display.set_caption("The Bot is on Fire!")

    graph = g.ManhattanGraph(screen, cnt.GRID_SIZE)
    graph.create_manhattan_graph()

    running = True
    steps = 0

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
                        if not graph.canProceed:
                            print("Wait for the action to be complete!")
                            pass
                        if graph.game_over:
                            graph = g.ManhattanGraph(screen, cnt.GRID_SIZE)
                            graph.create_manhattan_graph()
                            graph.proceed()
                        else:
                            graph.canProceed = False
                            while graph.step == 1:
                                graph.proceed()
                                time.sleep(0)
                            while graph.step == 5 and not graph.game_over:
                                steps += 1
                                graph.proceed()
                                time.sleep(cnt.TIME_RATE)
                            else:
                                # Generate report
                                graph.proceed()
                                graph.canProceed = True

                                q = cnt.FIRE_RESISTANCE_QUOTIENT
                                isFirePutOut = graph.curr_bot_pos == graph.curr_button_pos
                                print(f"Steps taken is {steps}")
                                print(f"The Value of Q is {q}")
                                if isFirePutOut:
                                    print(f"Fire has been PUT OUT {isFirePutOut}")
                                else:
                                    print(f"Fire has NOT been PUT OUT {isFirePutOut}")
                                steps = 0
        draw_grid(screen, graph, cnt.GRID_SIZE)

    pygame.quit()