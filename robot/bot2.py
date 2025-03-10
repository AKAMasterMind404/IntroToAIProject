from helpers.generic import HelperService
from robot.robot import Robot


class Bot2(Robot):
    def __init__(self):
        super().__init__()
        self.bot_type = 2
        self.avoid_fire_cells = True
        self.avoid_adjacent_fire_cells = False
        
    def compute_path(self):
        return super().compute_path()

    def moveBot(self):
        graph = self.graph
        """Moves the bot one step while dynamically avoiding fire."""

        # Check if the next step is blocked by fire
        if not graph.path or len(graph.path) < 2 or graph.fire_nodes.intersection(list(graph.path)):
            HelperService.printDebug("Fire detected ahead! Recalculating path...")
            graph.path = self.compute_path()

            # Stop moving if no valid path exists
            if not graph.path or len(graph.path) < 2:
                HelperService.printDebug("No safe path. Bot cannot move.")
                return False

        # Move bot one step forward
        graph.curr_bot_pos = graph.path[1]
        graph.path.pop(0)

        HelperService.printDebug(f" Bot moved to {graph.curr_bot_pos}")
        return True