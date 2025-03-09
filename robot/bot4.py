from graph.astar import astar
from helpers.generic import HelperService
from robot.robot import Robot
import networkx as nx
import copy
import constants as cnt


class Bot4(Robot):
    def __init__(self):
        super().__init__()
        self.bot_type = 4
        self.avoid_fire_cells = True
        self.avoid_adjacent_fire_cells = True

    def compute_path(self):
        graph = self.graph
        G_temp = graph.Ship.copy()
        source = graph.curr_bot_pos
        target = graph.curr_button_pos

        unwanted = graph.fire_nodes
        for node in graph.Ship.nodes:
            if node in {graph.curr_bot_pos, graph.curr_button_pos}:
                continue  # Ensure the bot's current position & button are NEVER removed
            if graph.Ship.nodes[node]['weight'] == 1 or node in unwanted:
                G_temp.remove_node(node)
        try:
            # Simulating fire
            graph = copy.copy(self.graph)
            for _ in range(5):
                graph.spreadFire()

            newFire = graph.fire_nodes - self.graph.fire_nodes
            newAdjFire = set(graph.nodes_with_burning_neighbours.keys()) - set(self.graph.nodes_with_burning_neighbours.keys())
            self.graph.fire_forecast = newFire
            self.graph.adj_fire_forecast = newAdjFire

            # Calculating path
            path = astar(G_temp, source, target, self.fire_aware_heuristic)
            return path
        except nx.NetworkXNoPath:
            HelperService.printDebug("No path available to the button!")
            return []

    def fire_aware_heuristic(self, node1, node2):
        distance = abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])  # Manhattan distance
        fire_danger = self.calculateDanger(node1)
        return distance + cnt.ALPHA*fire_danger

    def calculateDanger(self, cell: tuple):
        graph = self.graph
        danger = 0
        for neighbor in HelperService.getAllOpenNeighbours(graph.Ship, cell, self.graph.n):
            if neighbor not in graph.Ship.nodes:
                HelperService.printDebug(f"Warning: {neighbor} is not in graph.nodes!")  # Debugging
                continue

            if neighbor in graph.fire_nodes:
                danger += 1
            elif neighbor in graph.nodes_with_burning_neighbours.keys():
                danger += 0.5
            elif neighbor in graph.fire_forecast:
                danger += 0.3
            elif neighbor in graph.adj_fire_forecast:
                danger += 0.2

        return danger

    def moveBot(self):
        path = self.compute_path()
        if not path:
            HelperService.printDebug("No valid path found.")
            return self.graph.curr_bot_pos  # Stay in place

        next_step = path[1] if len(path) > 1 else path[0]
        self.graph.curr_bot_pos = next_step  # Move bot to next step
        self.graph.beenTo.append(next_step)
        return next_step