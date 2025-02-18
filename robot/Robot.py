import networkx as nx

from graph.graph import ManhattanGraph
from robot import bot1 as b1
from robot import bot2 as b2
from robot import bot3 as b3
from robot import bot4 as b4


class Robot:
    def __init__(self, graph: ManhattanGraph):
        self.bot_type = None
        self.graph = graph
        self.avoid_fire_cells = False
        self.avoid_adjacent_fire = False

    def compute_path(self):
        """Computes the safest path for Bot 3, either avoiding adjacent fire or just fire itself."""

        print(f"Computing path for Bot {self.bot_type}, with Avoid Fire cells: {self.avoid_fire_cells}"
              f" and Avoid fire neighbours: {self.avoid_adjacent_fire}")
        graph = self.graph
        G_temp = graph.Ship.copy()  # Work on a copy to keep the original graph intact

        # Determine which nodes to avoid
        unwanted = set()
        if self.avoid_fire_cells:
            unwanted = unwanted.union(graph.fire_nodes)
        if self.avoid_adjacent_fire:
            unwanted = unwanted.union(set(graph.nodes_with_burning_neighbours.keys()))

        for node in graph.Ship.nodes:
            if node in {graph.curr_bot_pos, graph.curr_button_pos}:
                continue  # Ensure the bot's current position & button are NEVER removed
            if graph.Ship.nodes[node]['weight'] == 1 or node in unwanted:
                G_temp.remove_node(node)

        try:
            return nx.shortest_path(G_temp, source=graph.curr_bot_pos, target=graph.curr_button_pos, weight='weight')
        except nx.NetworkXNoPath:
            print(" No path found!")
            return None

    def moveBot(self):
        pass

def RobotGateway(botType) -> Robot:
    if botType == 1:
        return b1.Bot1()
    if botType == 2:
        return b2.Bot2()
    if botType == 3:
        return b3.Bot3()
    # if botType == 4:
    #     return b4.Bot4()
    raise ValueError(f"Invalid botType: {botType}")