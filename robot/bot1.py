from robot.robot import Robot

class Bot1(Robot):
    def __init__(self):
        super().__init__()
        self.bot_type = 1
        self.avoid_fire_cells = False
        self.avoid_adjacent_fire = False

    def compute_path(self):
        return super().compute_path()

    def moveBot(self):
        # Recalculate path only if it's None
        graph = self.graph
        if graph.path is None:
            graph.path = self.compute_path()

        # If no valid path exists, stop
        if not graph.path or len(graph.path) == 0:
            return False

        # Move to the next step in the path
        next_pos = graph.path.pop(0)
        graph.curr_bot_pos = next_pos

        return True