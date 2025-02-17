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
        self.path = None
        self.screen = screen
        self.current_step = "Ship Expansion"
        self.one_neighbour_set = set()
        self.currently_open = set()
        self.multi_neighbour_set = set()
        self.dead_ends = []
        self.step = 1  # Track algorithm step
        self.open_ship_initialized = False
        self.fire_nodes = set()
        self.curr_bot_pos = None
        self.curr_button_pos = None

    def create_manhattan_graph(self):
        for i in range(self.n):
            for j in range(self.n):
                node = (i, j)
                self.G.add_node(node, weight=1)
                if i > 0:
                    self.G.add_edge(node, (i - 1, j), weight=1)
                if j > 0:
                    self.G.add_edge(node, (i, j - 1), weight=1)
        draw_grid(self.screen, self, self.n)

    def initialize_ship_opening(self):
        xCord = random.randint(1, self.n - 2)
        yCord = random.randint(1, self.n - 2)
        self.G.nodes[(xCord, yCord)]['weight'] = 0
        self.currently_open.add((xCord, yCord))
        self.one_neighbour_set = set(self.getEligibleNeighbours((xCord, yCord)))
        self.open_ship_initialized = True
        draw_grid(self.screen, self, self.n)

    def isNodeIsolated(self, node: tuple):
        x,y = node
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

        isOpenCount = 0
        for nX, nY in neighbors:
            node = self.G.nodes[(nX,nY)]
            if node['weight'] == 0:
                isOpenCount += 1

        if isOpenCount == 1:
            return True

    def getEligibleNeighbours(self, node):
        x, y = node
        neighbours = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        return [(cX, cY) for cX, cY in neighbours if
                0 < cX < self.n - 1 and 0 < cY < self.n - 1 and (cX, cY) not in self.currently_open]

    def proceed(self):
        if self.step == 1 and self.one_neighbour_set:
            cell_to_expand = random.choice(list(self.one_neighbour_set))
            self.G.nodes[cell_to_expand]['weight'] = 0
            self.currently_open.add(cell_to_expand)
            self.one_neighbour_set.remove(cell_to_expand)
            new_candidates = self.getEligibleNeighbours(cell_to_expand)
            for candidate in new_candidates:
                if candidate not in self.multi_neighbour_set:
                    if candidate in self.one_neighbour_set:
                        self.one_neighbour_set.remove(candidate)
                        self.multi_neighbour_set.add(candidate)
                    else:
                        self.one_neighbour_set.add(candidate)
            if not self.one_neighbour_set:
                self.step = 2  # Move to dead-end detection
                self.current_step = "Identifying Dead Ends"
            draw_grid(self.screen, self, self.n)

        elif self.step == 2:
            self.dead_ends = [node for node in self.currently_open if self.isNodeIsolated(node)]
            self.step = 3  # Move to dead-end expansion
            self.current_step = "Expanding Dead Ends"
            draw_grid(self.screen, self, self.n)

        elif self.step == 3 and self.dead_ends:
            num_to_expand = len(self.dead_ends) // 2
            random.shuffle(self.dead_ends)
            for i in range(num_to_expand):
                dead_end = self.dead_ends[i]
                closed_neighbors = [neighbor for neighbor in self.getEligibleNeighbours(dead_end) if
                                    self.G.nodes[neighbor]['weight'] == 1]
                if closed_neighbors:
                    to_open = random.choice(closed_neighbors)
                    self.G.nodes[to_open]['weight'] = 0
                    self.currently_open.add(to_open)
            self.step = 4
            self.current_step = "Algorithm Complete"
            draw_grid(self.screen, self, self.n)
        elif self.step == 4:
            opened_nodes = list(self.currently_open)

            fire_square = random.choice(opened_nodes)
            self.fire_nodes.add(fire_square)
            opened_nodes.remove(fire_square)

            bot_square = random.choice(opened_nodes)
            self.curr_bot_pos = bot_square
            opened_nodes.remove(bot_square)

            button_square = random.choice(opened_nodes)
            self.curr_button_pos = button_square

            draw_grid(self.screen, self, self.n)
            self.step = 5
        elif self.step == 5:
            pass


def draw_grid(screen, graph, n):
    screen.fill(cnt.WHITE)
    font = pygame.font.SysFont(None, 30)
    text = font.render(graph.current_step, True, cnt.BLACK)
    screen.blit(text, (20, 10))

    for i in range(n):
        for j in range(n):
            x = j * (cnt.CELL_SIZE + cnt.MARGIN)
            y = i * (cnt.CELL_SIZE + cnt.MARGIN) + cnt.HEADER_HEIGHT
            node = (i, j)

            if graph.G.nodes[node]['weight'] == 0:
                color = cnt.WHITE
            else:
                color = cnt.BLACK

            if node in graph.one_neighbour_set:
                color = cnt.YELLOW
            if node in graph.dead_ends and graph.step < 4:
                color = cnt.RED
            if node in graph.currently_open and (node not in graph.dead_ends and graph.step < 3):
                color = cnt.GREEN
            if node in graph.fire_nodes:
                color = cnt.RED
            if node == graph.curr_bot_pos:
                color = cnt.BLUE
            if node == graph.curr_button_pos:
                color = cnt.GREEN

            pygame.draw.rect(screen, color, (x, y, cnt.CELL_SIZE, cnt.CELL_SIZE))
            pygame.draw.rect(screen, cnt.GRAY, (x, y, cnt.CELL_SIZE, cnt.CELL_SIZE), 1)

    # Draw "Proceed" button
    pygame.draw.rect(screen, cnt.BLUE, (cnt.SCREEN_SIZE[0] // 2 - 50, cnt.SCREEN_SIZE[1] - 40, 100, 30))
    text = font.render("Proceed", True, cnt.WHITE)
    screen.blit(text, (cnt.SCREEN_SIZE[0] // 2 - 30, cnt.SCREEN_SIZE[1] - 35))

    pygame.display.flip()