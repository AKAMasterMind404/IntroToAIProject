import constants as cnt
from graph.graph import getGraph

def auto_game(q = cnt.FIRE_RESISTANCE_QUOTIENT, bot_type: int = 1, ipCells: set = None):
    graph = getGraph(None, bot_type, q, ipCells)
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
