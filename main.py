import graph.graph as g

if __name__ == "__main__":
    n = 60
    G = g.create_manhattan_graph(n)
    g.visualize_manhattan_graph(G, n)