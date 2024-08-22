# Exercício Laboratório 4 de Teoria dos Grafos
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

    def add_node(self, node) -> None:
        self.lista_adj[node] = {}
        self.order += 1

    def add_neighbor(self, node, node_neighbor, distance) -> None:
        self.lista_adj[node][node_neighbor] = distance
        self.size += 1

    def sort_nodes(self) -> None:
        self.lista_adj = dict(sorted(self.lista_adj.items()))

    def set_degree_list(self) -> None:
        for neighbors in self.lista_adj.values():
            self.degree_list.append(len(neighbors))

def dijkstra(graph, initial_node, final_node):
    distances = {node: float('inf') for node in graph}
    distances[initial_node] = 0

    previous_nodes = {node: None for node in graph}

    unvisited_nodes = list(graph.keys())

    while unvisited_nodes:
        # Encontra o nó com a menor distância
        min_node = None
        for node in unvisited_nodes:
            if min_node is None or distances[node] < distances[min_node]:
                min_node = node

        if distances[min_node] == float('inf'):
            break

        unvisited_nodes.remove(min_node)

        # Atualiza as distâncias para os nós vizinhos
        for neighbor, weight in graph[min_node].items():
            new_distance = distances[min_node] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = min_node

    # Constrói o caminho mais curto
    path = []
    current_node = final_node
    while current_node is not None:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]

    if distances[final_node] == float('inf'):
        return None, []
    else:
        return distances[final_node], path


def main():
    graph = Graph()

    # primeira linha de entrada (size do grafo)
    graph.size = int(input())

    # arestas do grafo
    for i in range(graph.size):
        edge = input()
        nodes = list(map(int, edge.split(' ')))

        # adicionar o vizinho no primeiro vértice
        if not graph.search_node(nodes[0]):
            graph.add_node(nodes[0])
        graph.add_neighbor(nodes[0], nodes[1], nodes[2])

        if not graph.search_node(nodes[1]):
            graph.add_node(nodes[1])


    n_centros_distribuicao = int(input())
    centros_distribuicao = []

    for i in range(n_centros_distribuicao):
        centro_distribuicao = input().split(' ')
        if (centro_distribuicao[1] != '0'):
            centros_distribuicao.append(int(centro_distribuicao[0]))

    cidade_cliente = int(input())

    shortest_distance = float('inf')
    shortest_path = []
    ct_chosen = 0
    for ct in centros_distribuicao:
        distance, path = dijkstra(graph.lista_adj, ct, cidade_cliente)
        if distance == None:
            next
        else:
            if distance < shortest_distance:
                shortest_distance = distance
                shortest_path = path
                ct_chosen = ct

    if not shortest_path:
        print(f"Nao ha rotas para {cidade_cliente} ou o produto em estoque")
    else:
        print(f"{ct_chosen} {int(shortest_distance / 100)}")
        print(" ".join(map(str, shortest_path)))

main()