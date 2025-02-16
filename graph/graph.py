import pygame
import networkx as nx
import random
import constants as cnt

class ManhattanGraph:
    def __init__(self, screen, n):
        self.n = n
        self.G = nx.Graph()
        self.start = (0, 0)
        self.goal = (n - 1, n - 1)
        self.path = None # self.compute_path()
        self.screen = screen

    def create_manhattan_graph(self):
        """Creates an NXN Manhattan graph with all nodes having weight = 0 (no obstacles)."""
        for i in range(self.n):
            for j in range(self.n):
                node = (i, j)
                self.G.add_node(node, weight=1) # Initialize all nodes as walkable
                # Connect Manhattan neighbors
                if i > 0:
                    self.G.add_edge(node, (i - 1, j), weight=1)
                if j > 0:
                    self.G.add_edge(node, (i, j - 1), weight=1)

        self._open_ship_cells()
        return self.G

    @staticmethod
    def getEligibleNeighbours(node: tuple, currently_open: set, n: int):
        x, y = node

        neighbours = []
        for cX, cY in [(x+1, y),(x-1,y),(x, y-1), (x, y+1)]:
            if 0 <= cX < n and 0 <= cY < n and (cX,cY) not in currently_open:
                neighbours.append((cX,cY))

        return neighbours

    def _open_ship_cells(self):
        n = self.n

        xCord = random.randint(1, n-1)
        yCord = random.randint(1, n-1)
        self.G.nodes[(xCord, yCord)]['weight'] = 0

        multi_neighbour_set:set = set()
        currently_open:set = set()
        one_neighbour_set:set = set(self.getEligibleNeighbours((xCord, yCord), currently_open, n))

        draw_grid(self.screen, self, n)

        while True:
            cell_to_expand = random.choice(list(one_neighbour_set))
            print(f"***** Cell to expand is:{cell_to_expand} *****")

            # Mark currently selected cell as open
            self.G.nodes[cell_to_expand]['weight'] = 0
            currently_open.add(cell_to_expand)

            # Check for eligible and non eligible cells and update respective sets
            x,y = cell_to_expand
            new_candidates = self.getEligibleNeighbours((x,y), currently_open, n)

            for candidate in new_candidates:
                eligibleToOpen = candidate not in multi_neighbour_set

                if eligibleToOpen:
                    if candidate in one_neighbour_set:
                        one_neighbour_set.remove(candidate)
                        multi_neighbour_set.add(candidate)
                    else:
                        one_neighbour_set.add(candidate)

            if len(one_neighbour_set) == 0:
                break

            draw_grid(self.screen, self, n)

    def compute_path(self):
        """Runs Dijkstra's algorithm, ensuring obstacle nodes are avoided."""
        G_temp = self.G.copy()  # Work on a copy to keep original graph intact

        # Remove all edges connected to obstacle nodes (weight = 1)
        for u, v in list(G_temp.edges):
            if self.G.nodes[u]['weight'] == 1 or self.G.nodes[v]['weight'] == 1:
                G_temp[u][v]['weight'] = float('inf')  # Make it unreachable

        try:
            return nx.shortest_path(G_temp, source=self.start, target=self.goal, weight='weight')
        except nx.NetworkXNoPath:
            return None

    def add_random_obstacle(self):
        """Randomly turns one free node into an obstacle (weight=1)."""
        free_nodes = [node for node in self.G.nodes if
                      self.G.nodes[node]['weight'] == 0 and node not in [self.start, self.goal]]
        if free_nodes:
            obstacle = random.choice(free_nodes)
            self.G.nodes[obstacle]['weight'] = 1
            self.path = self.compute_path()  # Recalculate shortest path
            draw_grid(self.screen, self, self.n)  # Refresh the grid

def draw_grid(screen, graph, n):
    """Draws the Manhattan grid using Pygame."""
    screen.fill(cnt.WHITE)  # Clear screen

    for i in range(n):
        for j in range(n):
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
