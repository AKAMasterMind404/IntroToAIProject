from robot.Robot import Robot


class Bot2(Robot):
    def __init__(self):
        super().__init__(super().graph)
        self.bot_type = 2
        self.avoid_fire_cells = True
        self.avoid_adjacent_fire = False
        
    def compute_path(self):
        return super().compute_path()

    def moveBot(self):
        graph = super().graph
        """Moves the bot one step while dynamically avoiding fire."""

        # Check if the next step is blocked by fire
        if not graph.path or len(graph.path) < 2 or graph.fire_nodes.intersection(list(graph.path)):
            print("Fire detected ahead! Recalculating path...")
            graph.path = self.compute_path()

            # Stop moving if no valid path exists
            if not graph.path or len(graph.path) < 2:
                graph.game_over = True
                print("No safe path. Bot cannot move.")
                return

        # Move bot one step forward
        graph.curr_bot_pos = graph.path[1]
        graph.path.pop(0)

        print(f" Bot moved to {graph.curr_bot_pos}")
