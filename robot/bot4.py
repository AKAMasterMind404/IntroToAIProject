from helpers.generic import HelperService
from robot.robot import Robot
import networkx as nx


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
            path = nx.astar_path(G_temp, source, target, heuristic=self.fire_aware_heuristic)
            return path
        except nx.NetworkXNoPath:
            HelperService.printDebug("No path available to the button!")
            return []

    def fire_aware_heuristic(self, node1, node2):
        distance = abs(node1[0] - node2[0]) + abs(node1[1] - node2[1])  # Manhattan distance
        fire_danger = self.calculateDanger(node1)
        return distance + fire_danger

    def calculateDanger(self, cell: tuple):
        graph = self.graph
        fire_nodes = graph.fire_nodes  # Nodes on fire
        adj_fire_nodes = graph.nodes_with_burning_neighbours.keys()  # Nodes next to fire
        danger = 0

        for neighbor in HelperService.getAllOpenNeighbours(graph.Ship, cell, self.graph.n):
            if neighbor not in graph.Ship.nodes:
                HelperService.printDebug(f"Warning: {neighbor} is not in graph.nodes!")  # Debugging
                continue

            if neighbor in fire_nodes:
                danger += 1
            elif neighbor in adj_fire_nodes:
                danger += 0.5

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