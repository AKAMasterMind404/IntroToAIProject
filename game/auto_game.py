import constants as cnt
from graph.graph import ManhattanGraph

def auto_game(graph: ManhattanGraph = None, q = cnt.FIRE_RESISTANCE_QUOTIENT, bot_type: int = 1):
    if not graph:
        graph = ManhattanGraph(None, cnt.GRID_SIZE, q, bot_type)
        graph.create_manhattan_graph()

    graph.initialize_ship_opening()
    if graph.game_over:
        graph = ManhattanGraph(None, cnt.GRID_SIZE, q, bot_type)
        graph.create_manhattan_graph()
        graph.proceed()
    else:
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
