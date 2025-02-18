from robot.robot import Robot


class Bot4(Robot):
    def __init__(self):
        super().__init__()
        self.bot_type = 4
        self.avoid_fire_cells = True
        self.avoid_adjacent_fire = True

    def compute_path(self):
        return super().compute_path()

    def moveBot(self):
        return super().moveBot()