import node as nd

class PriorityNode:
    def __init__(self, node: nd.Node, prevNode: nd.Node = None, nodeDist = float("inf")):
        self.nodeDist : float = nodeDist
        self.prevNode: nd.Node = prevNode
        self.node = node

    def __str__(self):
        return f"PriorityQueue : x:{self.node.x}, y:{self.node.y}, nodeDist:{self.nodeDist}"


class PriorityQueue:
    def __init__(self, manhattan_graph: dict):
        self.graph:dict = manhattan_graph
        self.minValue:float = float("inf")
        self.maxValue:float = float("inf")
        self.queue:dict = {}

    def createPriorityQueue(self):
        for x,y in self.graph.keys():
            dist = float("inf")
            if x == y == 0:
                dist = 0
            self.queue[(x,y)]=PriorityNode(node=nd.Node(x,y), nodeDist=dist)

        return self.queue