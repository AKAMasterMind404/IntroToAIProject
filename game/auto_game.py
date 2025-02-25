import constants as cnt
from graph.graph import ManhattanGraph

def auto_game(graph: ManhattanGraph = None):
    if not graph:
        graph = ManhattanGraph(None, cnt.GRID_SIZE)
        graph.create_manhattan_graph()

    graph.initialize_ship_opening()
    if graph.game_over:
        graph = ManhattanGraph(None, cnt.GRID_SIZE)
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
    return graph
