class Node:
    def __init__(self, x, y, dist = 1):
        self.x = x
        self.y = y
        self.dist = dist or 1
    
    def __str__(self):
        return f"Node : x:{self.x}, y:{self.y}, dist:{self.dist}"

if __name__ == "__main__":
    n = Node(1,2,5)
    print(n)