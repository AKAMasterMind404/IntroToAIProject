import networkx as nx
import matplotlib.pyplot as plt
import random

def create_manhattan_graph(n):
    G = nx.Graph()
    for i in range(n):
        for j in range(n):
            node = (i, j)
            weight = random.choice([0, 1])  # Assign weight 0 or 1
            G.add_node(node, weight=weight)

            # Connect valid Manhattan neighbors with weight 1
            if i > 0:
                G.add_edge(node, (i - 1, j), weight=1)
            if j > 0:
                G.add_edge(node, (i, j - 1), weight=1)

    return G

def visualize_manhattan_graph(G, n):
    pos = {(i, j): (j / n, -i / n) for i in range(n) for j in range(n)}  # Normalize positions
    
    plt.figure(figsize=(12, 12))

    # Scale node and edge size based on `n` to prevent overlap
    node_size = max(1, 30000 // (n * n))
    edge_width = max(0.1, 50 / n)

    # Draw edges with dynamic width
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=edge_width)

    # Draw nodes with colors based on weight
    black_nodes = [node for node in G.nodes if G.nodes[node]['weight'] == 1]
    white_nodes = [node for node in G.nodes if G.nodes[node]['weight'] == 0]

    nx.draw_networkx_nodes(G, pos, nodelist=black_nodes, node_size=node_size, node_color='black')
    nx.draw_networkx_nodes(G, pos, nodelist=white_nodes, node_size=node_size, node_color='white', edgecolors='black')

    plt.title(f"{n}x{n} Manhattan Graph with Binary Weights")
    plt.axis("off")
    plt.gca().set_aspect('equal')  # Ensure even spacing
    plt.show()
