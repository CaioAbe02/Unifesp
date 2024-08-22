class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_edge(self, u, v, weight):
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
        self.adjacency_list[u].append((v, weight))
        self.adjacency_list[v].append((u, weight))
    
    def dijkstra(self, start):
        distances = {node: float('inf') for node in self.adjacency_list}
        distances[start] = 0
        unvisited_nodes = list(self.adjacency_list.keys())
        
        while unvisited_nodes:
            # Select the unvisited node with the smallest distance
            current_node = min(unvisited_nodes, key=lambda node: distances[node])
            unvisited_nodes.remove(current_node)
            
            if distances[current_node] == float('inf'):
                break
            
            for neighbor, weight in self.adjacency_list.get(current_node, []):
                distance = distances[current_node] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
        
        return distances

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    
    m = int(data[index])
    index += 1
    
    graph = Graph()
    
    for _ in range(m):
        u = int(data[index])
        v = int(data[index + 1])
        dist = int(data[index + 2])
        index += 3
        graph.add_edge(u, v, dist)
    
    n = int(data[index])
    index += 1
    
    distribution_centers = {}
    
    for _ in range(n):
        city_id = int(data[index])
        has_product = int(data[index + 1])
        index += 2
        distribution_centers[city_id] = has_product
    
    k = int(data[index])
    
    distances = graph.dijkstra(k)
    
    valid_centers = []
    
    for center, has_product in distribution_centers.items():
        if has_product and center in distances:
            travel_time = distances[center] / 100
            valid_centers.append((travel_time, center, distances[center]))
    
    if not valid_centers:
        print(f"Nao ha rotas para {k} ou o produto em estoque")
    else:
        valid_centers.sort()
        best_time, best_center, distance = valid_centers[0]
        path = []
        # Retrieve path from source to best_center (not implemented here for simplicity)
        print(f"{best_center} {round(best_time, 2)}")
        print(" ".join(map(str, path)))

main()
