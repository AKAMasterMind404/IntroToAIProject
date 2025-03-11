import constants as cnt
from graph.graph import getGraph
from graph.sample.sample1 import currently_open_1, dead_ends_1

# A function that runs a simulation without screen / ui elements
def auto_game(q = cnt.FLAMMABILITY, bot_type: int = 1, isUseIpCells: bool = False, isUsePresetPos: bool = False):
    graph = getGraph(None, bot_type, q, isUseIpCells, isUsePresetPos)
    # Graph life cycle same as in UI GAME

    if isUseIpCells:
        graph.currently_open = currently_open_1
        graph.dead_ends_1 = dead_ends_1
    else:
        graph.initialize_ship_opening()

    graph.canProceed = False
    while graph.step < 5:
        graph.proceed()
    steps = 0
    while graph.step == 5 and not graph.game_over:
        steps += 1
        graph.proceed()
        # Generate report
    isFirePutOut = graph.curr_bot_pos == graph.curr_button_pos
    graph.isFireExtinguished = isFirePutOut
    return graph
