# Exercício Laboratório 2 de Teoria dos Grafos
# Nome: Caio S. Abe
# RA: 148131

# node -> vértice
# edge -> aresta

class Graph:
    def __init__(self) -> None:
        self.order = 0
        self.size = 0
        self.lista_adj = {}
        self.degree_list = []
        self.adjacency_matrix = []

    def search_node(self, node) -> bool:
        if node in self.lista_adj:
            return True
        return False

    def add_node(self, node) -> bool:
        self.lista_adj[node] = []

    def add_neighbor(self, node, node_neighbor) -> None:
        self.lista_adj[node].append(node_neighbor)
        self.order += 1

    def sort_nodes(self) -> None:
        self.lista_adj = dict(sorted(self.lista_adj.items()))

    def set_degree_list(self) -> None:
        for neighbors in self.lista_adj.values():
            self.degree_list.append(len(neighbors))

    def set_adjacency_matrix(self) -> None:
        print(self.lista_adj)

        for node, neighbors in self.lista_adj.items():
            row = [0] * self.size

            for neighbor in neighbors:
                index = list(self.lista_adj.keys()).index(neighbor)
                row[index] = 1

            self.adjacency_matrix.append(row)

        print(self.adjacency_matrix)


def find_cycles() -> None:
    pass


def main():
    graph = Graph()

    # primeira linha de entrada (size do grafo)
    graph.size = int(input())

    # arestas do grafo
    for i in range(graph.size):
        edge = input()
        nodes = edge.split(' ')

        # adicionar o vizinho no primeiro vértice
        if not graph.search_node(nodes[0]):
            graph.add_node(nodes[0])
        graph.add_neighbor(nodes[0], nodes[1])

        # adicionar o vizinho do segundo vértice
        if not graph.search_node(nodes[1]):
            graph.add_node(nodes[1])
        graph.add_neighbor(nodes[1], nodes[0])

    graph.sort_nodes()
    graph.set_degree_list()
    graph.set_adjacency_matrix()

main()