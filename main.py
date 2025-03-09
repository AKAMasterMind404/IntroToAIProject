from game.ui_game import ui_game
from result.analysis import Result
import constants as cnt

if __name__ == "__main__":
    IS_DATA = True
    if IS_DATA:
        isPlot = False
        if isPlot:
            Result.botWiseAnalysis(cnt.CURRENT_BOT)
        else:
            print("Data gen started....")
            recordsToFill = 1000
            dataMap = Result.getFillRecordQuantity()
            Result.fillRecordsSimple(recordsToFill)
            print("Data gen finished....")
    else:
        g = ui_game(q=0.7, bot_type=cnt.CURRENT_BOT)
