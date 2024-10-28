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
        nodes = list(self.lista_adj.keys())

        left = 0
        right = len(nodes) - 1

        while left <= right:
            mid = (left + right) // 2

            if nodes[mid] == node:
                return True
            elif nodes[mid] > node:
                right = mid - 1
            else:
                left = mid + 1

        return False

    def add_node(self, node) -> bool:
        self.lista_adj[node] = []
        self.order += 1
        self.sort_nodes()

    def sort_nodes(self) -> None:
        self.lista_adj = dict(sorted(self.lista_adj.items()))

    def search_add_neighbor(self, node, neighbor) -> None:
        node_neighbors = self.lista_adj[node]

        left = 0
        right = len(node_neighbors) - 1

        while left <= right:
            mid = (left + right) // 2

            if neighbor < node_neighbors[mid]:
                right = mid - 1

            elif neighbor > node_neighbors[mid]:
                left = mid + 1

            else:
                node_neighbors.insert(mid + 1, neighbor)
                return

        node_neighbors.insert(left, neighbor)

    def search_neighbor(self, node, neighbor) -> bool:
        node_neighbors = self.lista_adj[node]

        left = 0
        right = len(node_neighbors) - 1

        while left <= right:
            mid = (left + right) // 2

            if node_neighbors[mid] == neighbor:
                return True
            elif node_neighbors[mid] > neighbor:
                right = mid - 1
            else:
                left = mid + 1

        return False

    def set_degree_list(self) -> None:
        for neighbors in self.lista_adj.values():
            self.degree_list.append(len(neighbors))

    def calculate_mean(self) -> None:
        sum = 0

        for degree in self.degree_list:
            sum += degree

        return format((sum / len(self.degree_list)), '.1f')


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
        graph.search_add_neighbor(nodes[0], nodes[1])

        # adicionar o vizinho do segundo vértice
        if not graph.search_node(nodes[1]):
            graph.add_node(nodes[1])
        graph.search_add_neighbor(nodes[1], nodes[0])

    # aresta a ser consultada no grafo
    edge = input()
    nodes = edge.split(' ')
    verify_edge = graph.search_neighbor(nodes[0], nodes[1])

    graph.set_degree_list()

    print(f"Order: {graph.order}")
    print(f"Size: {graph.size}")
    print(f"Min degree: {min(graph.degree_list)}")
    print(f"Max degree: {max(graph.degree_list)}")
    print(f"Average degree: {graph.calculate_mean()}")
    print(f"Degree list: {graph.degree_list}")

    for node, neighbors in graph.lista_adj.items():
        print(f"{node}: {neighbors}")

    print(verify_edge)

main()