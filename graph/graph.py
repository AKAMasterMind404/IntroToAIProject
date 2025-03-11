import networkx as nx
import random
import constants as cnt
import gateways.robotgateway as rg
import helpers.draw_grid as dg
from graph.sample.sample1 import dead_ends_1, currently_open_1, fire_pos_1, bot_pos_1, button_pos_1
from helpers.generic import HelperService
from robot.robot import Robot


class ManhattanGraph:
    def __init__(self, screen, n, q, bot_type, isUseIpCells:bool = False, isUsePresetPos: bool = False):
        self.n = n # Dimension of rhe 2d graph
        self.q = q # Flammability
        self.bot_type = bot_type # bot type
        self.game_over = False # Indicates whether game may or may not be proceeded
        self.Ship = nx.Graph() # Graph nodes represented using networkx.Graph object
        self.path = None # Path outlined by the bot
        self.canProceed = True # Indicates whether simulation is already under progress
        self.screen = screen # pygame.screen - May or may not be None
        self.current_step = "Ship Expansion" # Display Label
        self.one_neighbour_set = set() # Set of nodes with one 'open' cell, # Zero indicates 'open' and One indicates 'close'
        self.currently_open = set() # Nodes that are 'open', # Zero indicates 'open' and One indicates 'close'
        self.multi_neighbour_set = set() # Converse of one_neighbour_set
        self.dead_ends = [] # cells that have 3 closed cells around them
        self.step = 1  # Track algorithm step
        self.open_ship_initialized = False # Indicates whether step is completed or not, useful in preset metric graphs
        self.fire_nodes = set() # Nodes currently under fire
        self.nodes_with_burning_neighbours = dict() # Nodes that are adjacent to atleast one node on 'fire'
        self.curr_bot_pos = None # Current position of bot
        self.initial_fire_position = None # Initial position of fire
        self.curr_button_pos = None # Current and final button position
        self.isFireExtinguished = None # Variable that checks whether bot has extinguished the fire or not
        self.beenTo = [] # Tracks the footsteps of bot
        self.fire_forecast = [] # A set of cells that could be on fire in the future
        self.adj_fire_forecast = [] # A set of cells that could be adjacent to nodes on fire in the future
        self.isUseIpCells = isUseIpCells # A boolean flag indicating opened cells are already defined
        self.isUsePresetPos = isUsePresetPos # A boolean flag indicating fire, bot and button positions are already defined
        self.t = 0 # Time step, calculates how many times proceed() ahs been called. Also, a measure for no of steps taken by bot

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

        if self.isUseIpCells:
            xCord, yCord = random.choice(list(currently_open_1))
        else:
            xCord = random.randint(1, self.n - 2)
            yCord = random.randint(1, self.n - 2)
            self.one_neighbour_set = set(HelperService.getEligibleNeighbours(self, (xCord, yCord)))
        self.currently_open.add((xCord, yCord))
        self.Ship.nodes[(xCord, yCord)]['weight'] = 0
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
        # Everytime proceed is called, one timestep is increased.
        # Timestep counting begins when grid is set, and bot-button-fire is initialized
        if self.step == 1 and self.isUseIpCells:
            # Handles pre-defined graph values
            self.step = 4
            self.currently_open = currently_open_1
            self.dead_ends = dead_ends_1
            for i,j in self.dead_ends:
                self.Ship.nodes[(i,j)]['weight'] = 0
            return
        if self.step == 1 and self.one_neighbour_set:
            # Chose one cell to expand
            cell_to_expand = random.choice(list(self.one_neighbour_set))
            self.Ship.nodes[cell_to_expand]['weight'] = 0 # Zero indicates 'open' and One indicates 'close'
            self.currently_open.add(cell_to_expand)
            self.one_neighbour_set.remove(cell_to_expand)
            # one_neighbour_set is a set of nodes that are surrounded by just one open cell

            new_candidates = HelperService.getEligibleNeighbours(self, cell_to_expand)
            for candidate in new_candidates:
                if candidate not in self.multi_neighbour_set:
                    if candidate in self.one_neighbour_set:
                        self.one_neighbour_set.remove(candidate)
                        self.multi_neighbour_set.add(candidate)
                    else:
                        self.one_neighbour_set.add(candidate)
            if not self.one_neighbour_set:
                # We ran out of cells that we can expand into
                self.step = 2  # Move to dead-end detection
                self.current_step = "Identifying Dead Ends"
            _draw_grid_internal(self)

        elif self.step == 2:
            HelperService.printDebug(f"Step {self.step} has begun!!")
            self.dead_ends = [node for node in self.currently_open if self.isNodeIsolated(node)]
            self.step = 3  # Move to dead-end expansion
            self.current_step = "Expanding Dead Ends"
            _draw_grid_internal(self)

        elif self.step == 3:
            # We randomly open one closed neighbour of half of the dead end cells
            if self.dead_ends:
                HelperService.printDebug(f"Step {self.step} has begun!!")
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
                HelperService.printDebug("Dead ends not found!!")
            # Ship Generation is Complete!
            self.step = 4
            self.current_step = "Ship Generation Complete"
            _draw_grid_internal(self)
        elif self.step == 4:
            HelperService.printDebug(f"Step {self.step} has begun!!")
            opened_nodes = list(self.currently_open)

            if self.isUsePresetPos:
                fire_square, bot_square, button_square = fire_pos_1, bot_pos_1, button_pos_1
            else:
                fire_square, bot_square, button_square = random.sample(opened_nodes, 3)

            # Opening fire_square
            opened_nodes.remove(fire_square)
            self.initial_fire_position = fire_square
            self.fire_nodes.add(fire_square)
            self.nodes_with_burning_neighbours = self._findPotentialNeighbours(fire_square, self.nodes_with_burning_neighbours)

            # Opening bot_square
            self.curr_bot_pos = bot_square
            opened_nodes.remove(bot_square)

            # Opening button_square
            self.curr_button_pos = button_square

            self.current_step = "Placed the button, fire and the bot"
            _draw_grid_internal(self)
            self.step = 5
        elif self.step == 5:
            HelperService.printDebug(f"Step {self.step} has begun!!")
            self.t += 1
            # The Task

            # Step 1: Checking if the button or bot has caught fire
            if not self._checkIfButtonOrBotCaughtFire():
                self.game_over = True
                HelperService.printDebug("Cannot Proceed!")
                _draw_grid_internal(self)
                return

            # Step 2: Move the bot
            robot:Robot = rg.RobotGateway(self.bot_type)
            robot.setGraph(self)
            path = robot.moveBot()
            if not path:
                self.current_step = "No Path Found! Cannot proceed further!"
                self.game_over = True

            # Step 3: Check if the button is pressed
            if self._isButtonPressed():
                HelperService.printDebug("The Fire Has been Extinguished!")
                self.current_step = "The Fire Has been Extinguished!"
                self.game_over = True
                return
            else:
                if self.path is None and self.curr_button_pos != self.curr_button_pos and self.game_over:
                    self.current_step = "No Path Found! Cannot proceed!"
                    self.game_over = True
                self.spreadFire()

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

    def spreadFire(self):
        newFireyDict = self.nodes_with_burning_neighbours.copy()

        for x,y in newFireyDict.keys():
            neighbors = self.nodes_with_burning_neighbours[(x,y)]
            fire_luck = HelperService.calculateFireProbability(neighbors, self.q)
            randomNumber = random.random()

            isCatchFire = randomNumber < fire_luck
            if isCatchFire:
                self.fire_nodes.add((x,y))
                newFireyDict = self._findPotentialNeighbours((x, y), newFireyDict)
                self.nodes_with_burning_neighbours = newFireyDict

    def _checkIfButtonOrBotCaughtFire(self):
        if self.curr_button_pos in self.fire_nodes:
            HelperService.printDebug("Game over! The button is on fire")
            self.current_step = "Game over! The button is on fire"
            return False
        if self.curr_bot_pos in self.fire_nodes:
            self.current_step = "Game over! The Bot is on fire"
            HelperService.printDebug("Game over! The Bot is on fire!")
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

def getGraph(screen, bot_type, q, isUseIpCells: bool = False, isUsePresetPos: bool = False):
    graph = ManhattanGraph(screen, cnt.GRID_SIZE, q, bot_type=bot_type, isUseIpCells=isUseIpCells, isUsePresetPos=isUsePresetPos)
    graph.create_manhattan_graph()

    return graph