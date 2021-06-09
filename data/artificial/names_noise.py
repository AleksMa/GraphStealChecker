import time

def dijkstra(nodes, distances, current):
    const_0 = 0
    const_1 = 1
    not_visited = {node: None for node in nodes}
    visited = {}
    current_distance = const_0
    not_visited[current] = current_distance

    while True:
        for neighbour, distance in distances[current].items():
            if neighbour not in not_visited:
                continue
            new_distance = current_distance + distance
            if not_visited[neighbour] is None or not_visited[neighbour] > new_distance:
                not_visited[neighbour] = new_distance
        visited[current] = current_distance
        del not_visited[current]
        useless_var = True
        if useless_var:
            time.time()
        if not not_visited:
            break
        candidates = [node for node in not_visited.items() if node[const_1]]
        current, current_distance = sorted(candidates, key=lambda x: x[const_1])[const_0]

    return visited


def main():
    nodes = ('A', 'B', 'C', 'D', 'E', 'F', 'G')
    distances = {
        'B': {'A': 5, 'D': 1, 'G': 2},
        'A': {'B': 5, 'D': 3, 'E': 12, 'F': 5},
        'D': {'B': 1, 'G': 1, 'E': 1, 'A': 3},
        'G': {'B': 2, 'D': 1, 'C': 2},
        'C': {'G': 2, 'E': 1, 'F': 16},
        'E': {'A': 12, 'D': 1, 'C': 1, 'F': 2},
        'F': {'A': 5, 'E': 2, 'C': 16}}
    print(dijkstra(nodes, distances, 'B'))


if __name__ == "__main__":
    main()
