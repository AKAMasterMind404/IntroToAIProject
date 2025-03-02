from helpers.generic import HelperService
from robot.robot import Robot

class Bot3(Robot):
    def __init__(self):
        super().__init__()
        self.bot_type = 3
        self.avoid_fire_cells = True
        self.avoid_adjacent_fire = True

    def compute_path(self):
        return super().compute_path()

    def moveBot(self):
        """Moves Bot 3 by dynamically avoiding fire and re-planning if necessary."""
        # Define the set of unwanted nodes (fire + adjacent to fire)
        graph = self.graph
        primary_unwanted = set(graph.nodes_with_burning_neighbours.keys()).union(graph.fire_nodes)

        # Recalculate path if:
        # - No existing path
        # - The path is too short to move
        # - The next step is in an unwanted node
        if not graph.path or len(graph.path) < 2 or primary_unwanted.intersection(set(graph.path)):
            HelperService.printDebug("Fire detected! Recalculating safest path...")

            # First, try avoiding fire + adjacent burning nodes
            graph.path = self.compute_path()

            # If no path exists, try avoiding only fire nodes (not adjacent burning nodes)
            if not graph.path:
                HelperService.printDebug("No path avoiding adjacent fire! Recomputing with fire-only constraint...")
                graph.path = self.compute_path()

            # If still no path, bot is stuck
            if not graph.path or len(graph.path) < 2:
                HelperService.printDebug("No safe path found. Bot cannot move!")
                return False

        # Move bot one step forward
        graph.curr_bot_pos = graph.path[1]  # Move to the next position
        graph.path.pop(0)  # Remove the step taken

        HelperService.printDebug(f"Bot 3 moved to {graph.curr_bot_pos}")
        return True