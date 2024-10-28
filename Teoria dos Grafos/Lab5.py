class Graph:
    def __init__(self) -> None:
        self.order = 0
        self.size = 0
        self.lista_adj = {}
        self.node_colors = {}
        self.degree_list = []

    def search_node(self, node) -> bool:
        return node in self.lista_adj

    def add_node(self, node) -> None:
        self.lista_adj[node] = []
        self.node_colors[node] = -1
        self.order += 1

    def add_neighbor(self, node, node_neighbor) -> None:
        self.lista_adj[node].append(node_neighbor)
        self.size += 1

    def sort_nodes(self) -> None:
        self.lista_adj = dict(sorted(self.lista_adj.items(), key=lambda item: (-len(item[1]), item[0])))

    def set_degree_list(self) -> None:
        for neighbors in self.lista_adj.values():
            self.degree_list.append(len(neighbors))

    def colorir(self) -> None:
        for node, neighbors in self.lista_adj.items():
            used_colors = {self.node_colors[neighbor] for neighbor in neighbors if self.node_colors[neighbor] != -1}

            color = 0
            while color in used_colors:
                color += 1

            self.node_colors[node] = color

        # Sort the node_colors dictionary by node
        self.node_colors = dict(sorted(self.node_colors.items()))

        for node, color in self.node_colors.items():
            print(f"{node} {color}")

def main():
    graph = Graph()

    # número de arestas do grafo
    num_arestas = int(input())

    # arestas do grafo
    for i in range(num_arestas):
        edge = input()
        nodes = list(map(int, edge.split(' ')))

        # adicionar o vizinho no primeiro vértice
        if not graph.search_node(nodes[0]):
            graph.add_node(nodes[0])
        graph.add_neighbor(nodes[0], nodes[1])

        if not graph.search_node(nodes[1]):
            graph.add_node(nodes[1])
        graph.add_neighbor(nodes[1], nodes[0])

    graph.sort_nodes()
    graph.colorir()

main()
