from abc import abstractmethod
import networkx as nx
from graph.djikstras import compatibleGraph, getPathFromATOB, djikstras
from helpers.generic import HelperService

class Robot:
    def __init__(self):
        self.bot_type = None
        self.graph = None
        self.avoid_fire_cells = False
        self.avoid_adjacent_fire_cells = False

    @abstractmethod
    def setGraph(self, graph):
        self.graph = graph

    def compute_path(self):
        """Computes the safest path for Bot 3, either avoiding adjacent fire or just fire itself."""

        HelperService.printDebug(
            f"Computing path for Bot {self.bot_type}, with Avoid Fire cells: {self.avoid_fire_cells}"
            f" and Avoid fire neighbours: {self.avoid_adjacent_fire_cells}")
        graph = self.graph
        G_temp: nx.Graph = graph.Ship.copy()  # Work on a copy to keep the original graph intact

        # Determine which nodes to avoid
        unwanted = set()
        if self.graph.t == 1 or self.avoid_fire_cells:
            unwanted = unwanted.union(graph.fire_nodes)
        if self.avoid_adjacent_fire_cells:
            unwanted = unwanted.union(set(graph.nodes_with_burning_neighbours.keys()))

        for node in graph.Ship.nodes:
            if node in {graph.curr_bot_pos, graph.curr_button_pos}:
                continue  # Ensure the bot's current position & button are NEVER removed
            if graph.Ship.nodes[node]['weight'] == 1 or node in unwanted:
                G_temp.remove_node(node)

        try:
            adj_list = list(G_temp.adjacency())
            comp_graph = compatibleGraph(adj_list)
            queue = djikstras(comp_graph, startNode=graph.curr_bot_pos)
            if queue is None:
                HelperService.printDebug("No valid queue returned from Dijkstra's algorithm!")
                return []
            path = getPathFromATOB(queue, graph.curr_bot_pos, graph.curr_button_pos)
            HelperService.printDebug(f"Path is {path}")
            return path
        except nx.NetworkXNoPath:
            HelperService.printDebug(" No path found!")
            return None

    def moveBot(self):
        pass
