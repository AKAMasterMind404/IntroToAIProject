import pygame
import constants as cnt

def draw_grid(screen, game, n):
    screen.fill(cnt.WHITE)
    font = pygame.font.SysFont(None, 30)
    text = font.render(game.current_step, True, cnt.BLACK)
    screen.blit(text, (20, 10))

    for i in range(n):
        for j in range(n):
            x = j * (cnt.CELL_SIZE + cnt.MARGIN)
            y = i * (cnt.CELL_SIZE + cnt.MARGIN) + cnt.HEADER_HEIGHT
            node = (i, j)

            if game.Ship.nodes[node]['weight'] == 0:
                color = cnt.WHITE
            else:
                color = cnt.BLACK

            if node in game.nodes_with_burning_neighbours.keys():
                intensity = game.nodes_with_burning_neighbours[node]
                if intensity == 1:
                    color = cnt.ORANGE
                elif intensity == 2:
                    color = cnt.D1_ORANGE
                elif intensity == 3:
                    color = cnt.D2_ORANGE
            if node in game.one_neighbour_set:
                color = cnt.YELLOW
            if node in game.dead_ends and game.step < 4:
                color = cnt.RED
            if node in game.currently_open and (node not in game.dead_ends and game.step < 3):
                color = cnt.GREEN
            if node in (game.path or []):
                color = cnt.YELLOW
            if node in game.fire_nodes:
                color = cnt.RED
            if node == game.curr_bot_pos:
                color = cnt.BLUE
            if node == game.curr_button_pos:
                color = cnt.GREEN

            pygame.draw.rect(screen, color, (x, y, cnt.CELL_SIZE, cnt.CELL_SIZE))
            pygame.draw.rect(screen, cnt.GRAY, (x, y, cnt.CELL_SIZE, cnt.CELL_SIZE), 1)

    # Draw "Proceed" button
    pygame.draw.rect(screen, cnt.BLUE, (cnt.SCREEN_SIZE[0] // 2 - 50, cnt.SCREEN_SIZE[1] - 40, 100, 30))
    message =  "Proceed" if game.canProceed else "Loading ..."
    if game.game_over: message = "Restart"
    text = font.render(message, True, cnt.WHITE)
    screen.blit(text, (cnt.SCREEN_SIZE[0] // 2 - 30, cnt.SCREEN_SIZE[1] - 35))

    pygame.display.flip()