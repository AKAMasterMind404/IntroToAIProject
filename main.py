import priorityQueue as pq
import node as nd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

def create_manhattan_graph(n):
    graph = defaultdict(list)

    for i in range(n):
        for j in range(n):
            node = (i, j)

            # Add only valid neighbors (Manhattan distance = 1)
            if i > 0:
                graph[node].append((i - 1, j))  # Up
            if i < n - 1:
                graph[node].append((i + 1, j))  # Down
            if j > 0:
                graph[node].append((i, j - 1))  # Left
            if j < n - 1:
                graph[node].append((i, j + 1))  # Right

    return graph

def visualize_manhattan_graph(G, n):
    pos = {(i, j): (j, -i) for i in range(n) for j in range(n)}  # Arrange nodes in a grid layout

    # Extract weights
    node_weights = nx.get_node_attributes(G, 'weight')

    plt.figure(figsize=(10, 10))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color=list(node_weights.values()), cmap=plt.cm.Blues)
    
    # Draw edge labels
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # Draw node weights
    nx.draw_networkx_labels(G, pos, labels=node_weights, font_color="black", font_size=8)
    
    plt.title(f"{n}x{n} Manhattan Grid Graph with Weights")
    plt.show()


def djikstras(graph: dict, pQueue: pq.PriorityQueue, start: nd.Node, end: nd.Node):
    if not graph.get(start) or not graph.get(end):
        print("Error!! Start or end node not found!")
    print("Start and End nodes found!")
    
    currNode = start
    visited = set()

    neighBourList = graph.get(currNode)
    pass
    # while len(visited) != len(graph.keys()):
    #     pass

def createPriorityQueue(graph: dict):
    pQueue = pq.PriorityQueue(graph)
    ans = pQueue.createPriorityQueue()

    return ans


if __name__ == "__main__":
    n = 4
    manhattan_graph = create_manhattan_graph(4)
    visualize_manhattan_graph(manhattan_graph, n)
    # [print(i) for i in manhattan_graph.items()]
    # priorityQueue = createPriorityQueue(manhattan_graph)
    # [print(i) for i in priorityQueue.items()]
    # djikstras(manhattan_graph, priorityQueue, nd.Node(0,0), nd.Node(3,3))