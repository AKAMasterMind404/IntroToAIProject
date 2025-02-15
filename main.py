import graph.graph as g
import pygame
import constants as cnt

if __name__ == "__main__":
    n = 30 # Grid size
    """Runs the Pygame event loop."""
    pygame.init()
    screen = pygame.display.set_mode(cnt.SCREEN_SIZE)
    pygame.display.set_caption("The Bot is on Fire!")

    graph = g.ManhattanGraph(n)
    running = True

    while running:
        g.draw_grid(screen, graph)  # Draw updated state

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit on close
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # Check if "Progress" button was clicked
                if cnt.SCREEN_SIZE[0] // 2 - 50 <= x <= cnt.SCREEN_SIZE[0] // 2 + 50 and cnt.SCREEN_SIZE[1] - 40 <= y <= cnt.SCREEN_SIZE[1] - 10:
                    graph.add_random_obstacle()  # Add obstacle & update path

    pygame.quit()
