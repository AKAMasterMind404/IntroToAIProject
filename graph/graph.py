import networkx as nx
import random
import constants as cnt
import gateways.robotgateway as rg
import helpers.draw_grid as dg
from helpers.generic import HelperService
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
        self.currentText = GraphHelper.getCurrentText(self.step)

    def create_manhattan_graph(self):
        for i in range(self.n):
            for j in range(self.n):
                node = (i, j)
                self.Ship.add_node(node, weight=1)
                if i > 0:
                    self.Ship.add_edge(node, (i - 1, j), weight=1)
                if j > 0:
                    self.Ship.add_edge(node, (i, j - 1), weight=1)

    def initialize_ship_opening(self):
        if self.open_ship_initialized:
            return
        xCord = random.randint(1, self.n - 2)
        yCord = random.randint(1, self.n - 2)
        self.Ship.nodes[(xCord, yCord)]['weight'] = 0
        self.currently_open.add((xCord, yCord))
        self.one_neighbour_set = set(HelperService.getEligibleNeighbours(self, (xCord, yCord)))
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

    def proceed(self):
        if self.step == 1 and self.one_neighbour_set:
            cell_to_expand = random.choice(list(self.one_neighbour_set))
            self.Ship.nodes[cell_to_expand]['weight'] = 0
            self.currently_open.add(cell_to_expand)
            self.one_neighbour_set.remove(cell_to_expand)
            new_candidates = HelperService.getEligibleNeighbours(self, cell_to_expand)
            for candidate in new_candidates:
                if candidate not in self.multi_neighbour_set:
                    if candidate in self.one_neighbour_set:
                        self.one_neighbour_set.remove(candidate)
                        self.multi_neighbour_set.add(candidate)
                    else:
                        self.one_neighbour_set.add(candidate)
            if not self.one_neighbour_set:
                self.step = 2  # Move to dead-end detection
                self.currentText = GraphHelper.getCurrentText(self.step)
            _draw_grid_internal(self)

        elif self.step == 2:
            print(f"Step {self.step} has begun!!")
            self.dead_ends = [node for node in self.currently_open if self.isNodeIsolated(node)]
            self.step = 3  # Move to dead-end expansion
            self.currentText = GraphHelper.getCurrentText(self.step)
            _draw_grid_internal(self)

        elif self.step == 3:
            if self.dead_ends:
                print(f"Step {self.step} has begun!!")
                num_to_expand = len(self.dead_ends) // 2
                random.shuffle(self.dead_ends)
                for i in range(num_to_expand):
                    dead_end = self.dead_ends[i]
                    closed_neighbors = [neighbor for neighbor in HelperService.getEligibleNeighbours(self, dead_end) if
                                        self.Ship.nodes[neighbor]['weight'] == 1]
                    if closed_neighbors:
                        to_open = random.choice(closed_neighbors)
                        self.Ship.nodes[to_open]['weight'] = 0
                        self.currently_open.add(to_open)
            else:
                print("Dead ends not found!!")
            self.step = 4
            self.currentText = GraphHelper.getCurrentText(self.step)
            _draw_grid_internal(self)

        elif self.step == 4:
            print(f"Step {self.step} has begun!!")
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

            self.step = 5
            self.currentText = GraphHelper.getCurrentText(self.step)
            _draw_grid_internal(self)
        elif self.step == 5:
            print(f"Step {self.step} has begun!!")
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
                self.currentText = GraphHelper.getCurrentText(8)
                self.game_over = True

            # Step 3: Check if the button is pressed
            if self._isButtonPressed():
                print("The Fire Has been Extinguished!")
                self.currentText = GraphHelper.getCurrentText(7)
                self.game_over = True
                return
            else:
                if self.path is None and self.curr_button_pos != self.curr_button_pos and self.game_over:
                    self.currentText = GraphHelper.getCurrentText(8)
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
        return self.curr_button_pos == self.curr_bot_pos

    def _spreadFire(self):
        newFireyDict = self.nodes_with_burning_neighbours.copy()

        for x,y in newFireyDict.keys():
            neighbors = self.nodes_with_burning_neighbours[(x,y)]
            fire_luck = HelperService.calculateFireProbability(neighbors)
            willLightUpLuck = random.random()

            isCatchFire = willLightUpLuck > fire_luck
            if isCatchFire:
                self.fire_nodes.add((x,y))
                newFireyDict = self._findPotentialNeighbours((x, y), newFireyDict)
                self.nodes_with_burning_neighbours = newFireyDict

    def _checkIfButtonOrBotCaughtFire(self):
        if self.curr_button_pos in self.fire_nodes:
            print("Game over! The button is on fire")
            self.currentText = GraphHelper.getCurrentText(9)
            return False
        if self.curr_bot_pos in self.fire_nodes:
            self.currentText = GraphHelper.getCurrentText(10)
            print("Game over! The Bot is on fire!")
            return False

        return True

    def _findPotentialNeighbours(self, fireNode: tuple, existingNeighbours: dict):
        neighbors = HelperService.getAllOpenNeighbours(self.Ship, fireNode, self.n)

        newFireDict = existingNeighbours.copy()
        for x, y in neighbors:
            node = self.Ship.nodes[(x, y)]
            if node["weight"] == 0:
                newFireDict[(x, y)] = newFireDict.get((x,y), 0) + 1

        return newFireDict

def _draw_grid_internal(graph: ManhattanGraph):
    dg.draw_grid(graph.screen, graph, graph.n)

class GraphHelper:
    @staticmethod
    def getCurrentText(code: int):
        text = "Ship Expansion"
        if code == 2:
            text = "Identifying Dead Ends"
        elif code == 3:
            text = "Expanding Dead Ends"
        elif code == 4:
            text = "Ship Generation Complete"
        elif code == 5:
            text = "Placed the button, fire and the bot"
        elif code == 6:
            text = "7 Path Found! Cannot proceed further!"
        elif code == 7:
            text = "The Fire Has been Extinguished!"
        elif code == 8:
            text = "No Path Found! Cannot proceed!"
        elif code == 9:
            text = "Game over! The button is on fire"
        elif code == 10:
            text = "Game over! The Bot is on fire"
        return text

    @staticmethod
    def getFreshGraph(screen):
        graph = ManhattanGraph(screen, cnt.GRID_SIZE)
        graph.create_manhattan_graph()
        return graph

    @staticmethod
    def openGraph(screen):
        graph = ManhattanGraph(screen, cnt.GRID_SIZE)
        graph.create_manhattan_graph()
        currently_open = set()
        for i in range(graph.n):
            for j in range(graph.n):
                if i in range(1, graph.n - 1) and j in range(1, graph.n - 1):
                    graph.Ship.nodes[(i, j)]['weight'] = 0
                    currently_open.add((i, j))
                else:
                    graph.Ship.nodes[(i, j)]['weight'] = 1
        graph.one_neighbour_set = set()
        graph.step = 4
        graph.currently_open = currently_open
        return graph