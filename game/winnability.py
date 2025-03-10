import constants as cnt
from graph.graph import getGraph
from graph.sample.sample1 import currently_open_1, dead_ends_1, bot_pos_1, button_pos_1, fire_pos_1


def winnability(q = cnt.FLAMMABILITY, bot_type: int = 1):
    graph = getGraph(None, bot_type, q, currently_open_1)

    if not cnt.IS_VARIABLE_GRAPH:
        graph.currently_open_1 = currently_open_1
        graph.dead_ends_1 = dead_ends_1

    while graph.step < 5:
        graph.proceed(bot_pos_1=bot_pos_1, button_pos_1=button_pos_1, fire_pos_1=fire_pos_1)
    steps = 0
    while graph.step == 5 and not graph.game_over:
        steps += 1
        graph.proceed()
    isFirePutOut = graph.curr_bot_pos == graph.curr_button_pos
    graph.isFireExtinguished = isFirePutOut
    return graph
