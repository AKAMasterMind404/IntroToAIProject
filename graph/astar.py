import heapq

def astar(graph, start, target, heuristic):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0

    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, target)

    while open_set:
        _, curVal = heapq.heappop(open_set)

        if curVal == target:
            path = []
            while curVal in came_from:
                path.append(curVal)
                curVal = came_from[curVal]
            path.append(start)
            return path[::-1]  # Return reversed path

        for neighbor in graph[curVal]:
            temp_g_val = g_score[curVal] + graph[curVal][neighbor].get("weight", 1)

            if temp_g_val < g_score[neighbor]:
                came_from[neighbor] = curVal
                g_score[neighbor] = temp_g_val
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, target)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None
