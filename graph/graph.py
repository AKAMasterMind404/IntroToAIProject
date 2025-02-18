import math
import pygame
import networkx as nx
import random
import constants as cnt
import gateways.robotgateway as rg
from robot.robot import Robot


class ManhattanGraph:
    def __init__(self, screen, n):
        self.n = n
        self.bot_type = cnt.CURRENT_BOT
        self.game_over = False
        self.Ship = nx.Graph()
        self.start = (0, 0)
        self.goal = (n - 1, n - 1)
        self.path = None
        self.canProceed = True
        self.screen = screen
        self.current_step = "Ship Expansion"
        self.one_neighbour_set = set()
        self.currently_open = set()
        self.multi_neighbour_set = set()
        self.dead_ends = []
        self.step = 1  # Track algorithm step
        self.open_ship_initialized = False
        self.fire_nodes = set()
        self.nodes_with_burning_neighbours = dict()
        self.curr_bot_pos = None
        self.initial_fire_position = None
        self.curr_button_pos = None

    def create_manhattan_graph(self):
        for i in range(self.n):
            for j in range(self.n):
                node = (i, j)
                self.Ship.add_node(node, weight=1)
                if i > 0:
                    self.Ship.add_edge(node, (i - 1, j), weight=1)
                if j > 0:
                    self.Ship.add_edge(node, (i, j - 1), weight=1)
        _draw_grid_internal(self)

    def initialize_ship_opening(self):
        xCord = random.randint(1, self.n - 2)
        yCord = random.randint(1, self.n - 2)
        self.Ship.nodes[(xCord, yCord)]['weight'] = 0
        self.currently_open.add((xCord, yCord))
        self.one_neighbour_set = set(self.getEligibleNeighbours((xCord, yCord)))
        self.open_ship_initialized = True
        _draw_grid_internal(self)

    def isNodeIsolated(self, node: tuple):
        x,y = node
        neighbors = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

        isOpenCount = 0
        for nX, nY in neighbors:
            node = self.Ship.nodes[(nX,nY)]
            if node['weight'] == 0:
                isOpenCount += 1

        if isOpenCount == 1:
            return True

    def getAllOpenNeighbours(self, node):
        x, y = node
        neighbours = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        return [(cX, cY) for cX, cY in neighbours if
                self.n - 1 > 0 < cX and 0 < cY < self.n - 1 and (cX, cY) and self.Ship.nodes[(cX, cY)]['weight'] == 0]

    def getEligibleNeighbours(self, node):
        x, y = node
        neighbours = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        return [(cX, cY) for cX, cY in neighbours if
                0 < cX < self.n - 1 and 0 < cY < self.n - 1 and (cX, cY) not in self.currently_open]

    def proceed(self):
        if self.step == 1 and self.one_neighbour_set:
            cell_to_expand = random.choice(list(self.one_neighbour_set))
            self.Ship.nodes[cell_to_expand]['weight'] = 0
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
            _draw_grid_internal(self)

        elif self.step == 2:
            self.dead_ends = [node for node in self.currently_open if self.isNodeIsolated(node)]
            self.step = 3  # Move to dead-end expansion
            self.current_step = "Expanding Dead Ends"
            _draw_grid_internal(self)

        elif self.step == 3 and self.dead_ends:
            num_to_expand = len(self.dead_ends) // 2
            random.shuffle(self.dead_ends)
            for i in range(num_to_expand):
                dead_end = self.dead_ends[i]
                closed_neighbors = [neighbor for neighbor in self.getEligibleNeighbours(dead_end) if
                                    self.Ship.nodes[neighbor]['weight'] == 1]
                if closed_neighbors:
                    to_open = random.choice(closed_neighbors)
                    self.Ship.nodes[to_open]['weight'] = 0
                    self.currently_open.add(to_open)
            self.step = 4
            self.current_step = "Ship Generation Complete"
            _draw_grid_internal(self)
        elif self.step == 4:
            opened_nodes = list(self.currently_open)

            fire_square = random.choice(opened_nodes)
            opened_nodes.remove(fire_square)
            self.initial_fire_position = fire_square
            self.fire_nodes.add(fire_square)
            self.nodes_with_burning_neighbours = self._findPotentialNeighbours(fire_square, self.nodes_with_burning_neighbours)

            bot_square = random.choice(opened_nodes)
            self.curr_bot_pos = bot_square
            opened_nodes.remove(bot_square)

            button_square = random.choice(opened_nodes)
            self.curr_button_pos = button_square

            self.current_step = "Placed the button, fire and the bot"
            _draw_grid_internal(self)
            self.step = 5
        elif self.step == 5:
            # The Task

            # Step 1: Checking if the button or bot has caught fire
            if not self._checkIfButtonOrBotCaughtFire():
                self.game_over = True
                print("Cannot Proceed!")
                _draw_grid_internal(self)
                return

            # Step 2: Move the bot
            robot:Robot = rg.RobotGateway(self.bot_type)
            robot.setGraph(self)
            path = robot.moveBot()
            if not path:
                self.game_over = True

            # Step 3: Check if the button is pressed
            if self._isButtonPressed():
                print("The Fire Has been Extinguished!")
                self.game_over = True
                return
            else:
                self._spreadFire()

            _draw_grid_internal(self)
            '''
            • The bot decides which open neighbor to move to.
            • The bot moves to that neighbor.
            • If the bot enters the button cell, the button is pressed and the fire is put out - the task is completed.
            • Otherwise, the fire advances.
            • If at any point the bot and the fire occupy the same cell, the task is failed.
            '''
            pass

    def _isButtonPressed(self):
        self.current_step = "The Fire Has been Extinguished!"
        return self.curr_button_pos == self.curr_bot_pos

    def _spreadFire(self):
        newFireyDict = self.nodes_with_burning_neighbours.copy()

        for x,y in newFireyDict.keys():
            neighbors = self.nodes_with_burning_neighbours[(x,y)]
            fire_luck = self._calculateFireProbablity(neighbors)
            willLightUpLuck = random.random()

            isCatchFire = willLightUpLuck > fire_luck
            if isCatchFire:
                self.fire_nodes.add((x,y))
                newFireyDict = self._findPotentialNeighbours((x, y), newFireyDict)
                self.nodes_with_burning_neighbours = newFireyDict

    def _checkIfButtonOrBotCaughtFire(self):
        if self.curr_button_pos in self.fire_nodes:
            print("Game over! The button is on fire")
            self.current_step = "Game over! The button is on fire"
            return False
        if self.curr_bot_pos in self.fire_nodes:
            self.current_step = "Game over! The Bot is on fire"
            print("Game over! The Bot is on fire!")
            return False

        return True

    def _findPotentialNeighbours(self, fireNode: tuple, existingNeighbours: dict):
        neighbors = self.getAllOpenNeighbours(fireNode)

        newFireDict = existingNeighbours.copy()
        for x, y in neighbors:
            node = self.Ship.nodes[(x, y)]
            if node["weight"] == 0:
                newFireDict[(x, y)] = newFireDict.get((x,y), 0) + 1

        return newFireDict

    def _calculateFireProbablity(self, neighbours):
        q = cnt.FIRE_RESISTANCE_QUOTIENT
        probability =  1 - math.pow(1 - q, neighbours)
        return probability

def _draw_grid_internal(graph: ManhattanGraph):
    draw_grid(graph.screen, graph, graph.n)

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