from game.ui_game import ui_game
from game.auto_game import auto_game
from graph.graph import ManhattanGraph
from result.analysis import Result
import constants as cnt

if __name__ == "__main__":
    # isPlot = True
    # if isPlot:
    #     Result.botWiseAnalysis(1)
    # else:
    #     recordsPerBot = 1000
    #     Result.fillRecords(recordsPerBot)
    g = ui_game(q=0.1, bot_type=cnt.CURRENT_BOT)
    print(g.Ship.nodes)
    print(g.currently_open)
