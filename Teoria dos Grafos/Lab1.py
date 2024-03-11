# Exercício Laboratório 1 de Teoria dos Grafos
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

    print(f"Order: {graph.order}")
    print(f"Size: {graph.size}")
    print(f"Degree list: {graph.degree_list}")

    for node, neighbors in graph.lista_adj.items():
        print(f"{node}: {neighbors}")

main()