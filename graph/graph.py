import pygame
import networkx as nx
import random
import constants as cnt

class ManhattanGraph:
    def __init__(self, n):
        self.n = n
        self.G = self.create_manhattan_graph()
        self.start = (0, 0)
        self.goal = (n - 1, n - 1)
        self.path = self.compute_path()

    def create_manhattan_graph(self):
        """Creates an NXN Manhattan graph with all nodes having weight = 0 (no obstacles)."""
        G = nx.Graph()
        for i in range(self.n):
            for j in range(self.n):
                node = (i, j)
                G.add_node(node, weight=0)  # Initialize all nodes as walkable

                # Connect Manhattan neighbors
                if i > 0:
                    G.add_edge(node, (i - 1, j), weight=1)
                if j > 0:
                    G.add_edge(node, (i, j - 1), weight=1)

        return G

    def compute_path(self):
        """Runs Dijkstra's algorithm, ensuring obstacle nodes are avoided."""
        G_temp = self.G.copy()  # Work on a copy to keep original graph intact

        # Remove all edges connected to obstacle nodes (weight = 1)
        for node in self.G.nodes:
            if self.G.nodes[node]['weight'] == 1:
                G_temp.remove_node(node)

        try:
            return nx.shortest_path(G_temp, source=self.start, target=self.goal, weight='weight')
        except nx.NetworkXNoPath:
            return None

    def add_random_obstacle(self):
        """Randomly turns one free node into an obstacle (weight=1)."""
        free_nodes = [node for node in self.G.nodes if self.G.nodes[node]['weight'] == 0 and node not in [self.start, self.goal]]
        if free_nodes:
            obstacle = random.choice(free_nodes)
            self.G.nodes[obstacle]['weight'] = 1
            self.path = self.compute_path()  # Recalculate shortest path

def draw_grid(screen, graph):
    """Draws the Manhattan grid using Pygame."""
    screen.fill(cnt.WHITE)  # Clear screen

    for i in range(graph.n):
        for j in range(graph.n):
            x = j * (cnt.CELL_SIZE + cnt.MARGIN)
            y = i * (cnt.CELL_SIZE + cnt.MARGIN)

            node = (i, j)
            color = cnt.WHITE  # Default is walkable

            if graph.G.nodes[node]['weight'] == 1:
                color = cnt.BLACK  # Obstacle
            elif node == graph.start:
                color = cnt.YELLOW  # Start
            elif node == graph.goal:
                color = cnt.RED  # Goal
            elif graph.path and node in graph.path:
                color = cnt.GREEN  # Shortest Path

            pygame.draw.rect(screen, color, (x, y, cnt.CELL_SIZE, cnt.CELL_SIZE))
            pygame.draw.rect(screen, cnt.GRAY, (x, y, cnt.CELL_SIZE, cnt.CELL_SIZE), 1)  # Grid outline

    # Draw the progress button
    pygame.draw.rect(screen, cnt.BLUE, (cnt.SCREEN_SIZE[0] // 2 - 50, cnt.SCREEN_SIZE[1] - 40, 100, 30))
    font = pygame.font.SysFont(None, 24)
    text = font.render("Progress", True, cnt.WHITE)
    screen.blit(text, (cnt.SCREEN_SIZE[0] // 2 - 30, cnt.SCREEN_SIZE[1] - 35))

    pygame.display.flip()  # Update screen

def start_gui(n):
    """Runs the Pygame event loop."""
    pygame.init()
    screen = pygame.display.set_mode(cnt.SCREEN_SIZE)
    pygame.display.set_caption("Manhattan Grid Progress")

    graph = ManhattanGraph(n)
    running = True

    while running:
        draw_grid(screen, graph)  # Draw updated state

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit on close
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                # Check if "Progress" button was clicked
                if cnt.SCREEN_SIZE[0] // 2 - 50 <= x <= cnt.SCREEN_SIZE[0] // 2 + 50 and cnt.SCREEN_SIZE[1] - 40 <= y <= cnt.SCREEN_SIZE[1] - 10:
                    graph.add_random_obstacle()  # Add obstacle & update path

    pygame.quit()
