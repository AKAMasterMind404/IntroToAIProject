def compatibleGraph(graph: list) -> dict:
    newGraph = dict()

    for node, neighbors in graph:
        newGraph[node] = []  # Initialize adjacency list for this node

        for neighbor, attr in neighbors.items():
            weight = attr.get('weight', 1)  # Default weight is 1 if not specified
            newGraph[node].append({'node': neighbor, 'dist': weight})

    return newGraph


def _findDistanceFromNode1ToNode2(graph: dict, node1: tuple, node2: tuple):
    if node1 == node2:
        raise NameError(f'Node 1 and Node 2 have the same value {node1}!')

    node2Neighbours = graph[node2]
    dist = float('inf')
    for nb in node2Neighbours:
        if nb['node'] == node1:
            dist = nb['dist']
    return dist


def _findCurr(queue: dict, visited: set):
    least = float('inf')
    curr = None

    for node in queue.keys():
        prop = queue[node]
        if prop['shortest'] < least and node not in visited:
            curr = node
            least = prop['shortest']

    return curr


def _createPriorityQueue(graph: dict, startNode: tuple):
    queue = dict()
    for node in graph.keys():
        shortest = 0 if node == startNode else float('inf')
        queue[node] = {'shortest': shortest, 'prev': None}

    return queue


def getPathFromATOB(queue:dict, A: tuple, B: tuple):
    path = []

    curr = B
    while curr != A:
        path.append(curr)
        next = queue.get(curr)
        if not next:
            break
        curr = next['prev']

    result = path
    return result[::-1]


def djikstras(graph: dict, startNode: tuple):
    visited = set()
    queue = _createPriorityQueue(graph, startNode)

    while len(visited) != len(graph.keys()):
        # Assign a node as current
        curr = _findCurr(queue, visited)
        if curr is None:  # Handle disconnected graphs
            break

        neighbours = [i for i in graph[curr] if i['node'] not in visited]

        for neighbour in neighbours:
            neighbourNode: tuple = neighbour['node']
            distFromNeighbourToCurr = _findDistanceFromNode1ToNode2(graph, curr, neighbourNode)
            currNodeShortestValue = queue[curr]['shortest']
            totalDistanceFromStartToNeighbour = distFromNeighbourToCurr + currNodeShortestValue

            if totalDistanceFromStartToNeighbour < queue[neighbourNode]['shortest']:
                queue[neighbourNode]['shortest'] = totalDistanceFromStartToNeighbour
                queue[neighbourNode]['prev'] = curr

        visited.add(curr)

    return queue