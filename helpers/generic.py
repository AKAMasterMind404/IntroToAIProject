import networkx as nx
import constants as cnt
import math

class HelperService:

    @staticmethod
    def printDebug(arg: str):
        if cnt.K_DEBUG_MODE:
            print(arg)

    @staticmethod
    def neighbours(node: tuple) -> list:
        x, y = node
        return [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]

    @staticmethod
    def getAllOpenNeighbours(graph: nx.Graph, node: tuple, n):
        ngh = HelperService.neighbours(node)
        return [(cX, cY) for cX, cY in ngh if
                n - 1 > 0 < cX and 0 < cY < n - 1 and (cX, cY) and graph.nodes[(cX, cY)]['weight'] == 0]

    @staticmethod
    def getEligibleNeighbours(graph, node: tuple):
        ngh = HelperService.neighbours(node)
        return [(cX, cY) for cX, cY in ngh if
                0 < cX < graph.n - 1 and 0 < cY < graph.n - 1 and (cX, cY) not in graph.currently_open]

    @staticmethod
    def calculateFireProbability(neighbours, q):
        probability =  1 - math.pow(1 - q, neighbours)
        return probability