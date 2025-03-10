from game.ui_game import ui_game
from graph.sample.sample1 import sample_ip_1
from result.analysis import Result
import constants as cnt

if __name__ == "__main__":
    IS_DATA = False
    if IS_DATA:
        isPlot = False
        if isPlot:
            Result.botWiseAnalysis(cnt.CURRENT_BOT)
        else:
            print("Data gen started....")
            recordsToFill = 100
            dataMap = Result.getFillRecordQuantity()
            Result.fillRecordsSimple(recordsToFill)
            print("Data gen finished....")
    else:
        ipCells:set = sample_ip_1
        g = ui_game(q=cnt.FLAMABILITY, bot_type=cnt.CURRENT_BOT, ipCells=ipCells)
