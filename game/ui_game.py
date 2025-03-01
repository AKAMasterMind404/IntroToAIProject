from symtable import Function
from graph.graph import GraphHelper, ManhattanGraph
from helpers.draw_grid import draw_grid
import pygame
import constants as cnt
import time

def ui_game(screen, graphFunction: () = GraphHelper.getFreshGraph):
    pygame.init()
    pygame.display.set_caption("The Bot is on Fire!")

    running = True
    steps = 0

    # Initializing graph, if not passed as a parameter
    graph = graphFunction(screen)

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
                    graph.initialize_ship_opening()
                    if not graph.canProceed:
                        print("Wait for the action to be complete!")
                        pass
                    if graph.game_over:
                        graph = graphFunction(screen)
                        draw_grid(screen, graph, graph.n)
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