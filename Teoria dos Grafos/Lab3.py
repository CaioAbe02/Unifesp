# Exercício Laboratório 3 de Teoria dos Grafos
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
        self.nodes = []

    def search_node(self, node) -> bool:
        if node in self.lista_adj:
            return True
        return False

    def add_node(self, node) -> bool:
        self.lista_adj[node] = []
        self.nodes.append(node)
        self.nodes.sort()

    def add_neighbor(self, node, node_neighbor) -> None:
        self.lista_adj.setdefault(node, []).append(node_neighbor)
        self.lista_adj[node].sort()
        self.order += 1

    def sort_nodes(self) -> None:
        self.lista_adj = dict(sorted(self.lista_adj.items()))

    def set_degree_list(self) -> None:
        for neighbors in self.lista_adj.values():
            self.degree_list.append(len(neighbors))

    def remove_edge(self, node1, node2) -> None:
        self.lista_adj[node1].remove(node2)
        self.lista_adj[node2].remove(node1)

        if (len(self.lista_adj[node1]) == 0):
            self.lista_adj.pop(node1)
            self.nodes.remove(node1)

        if (len(self.lista_adj[node2]) == 0):
            self.lista_adj.pop(node2)
            self.nodes.remove(node2)

    def generate_prufer_code(self) -> None:
        sequence = []

        while len(self.lista_adj) > 2:
            for node, neighbors in self.lista_adj.items():
                if len(neighbors) == 1:
                    sequence.append(min(neighbors))
                    self.remove_edge(node, min(neighbors))
                    break

        for node in sequence:
            print(node, end= ' ')
        print()

    def decode_prufer_code(self, prufer_code) -> None:
        prufer_code = list(map(int, prufer_code.split()))
        n = len(prufer_code)
        nodes = set(range(n + 2))

        for i in range(n):
            node = min(nodes - set(prufer_code))
            self.add_neighbor(prufer_code[0], node)
            self.add_neighbor(node, prufer_code[0])
            prufer_code.pop(0)
            nodes.remove(node)

        nodes = list(nodes)
        self.add_neighbor(nodes[0], nodes[1])
        self.add_neighbor(nodes[1], nodes[0])
        self.sort_nodes()
        for node, neighbors in self.lista_adj.items():
            print(f"{node}: {neighbors}")

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

    prufer_code = input()

    graph.sort_nodes()
    graph.set_degree_list()

    graph.generate_prufer_code()

    graph2 = Graph()
    graph2.decode_prufer_code(prufer_code)

main()