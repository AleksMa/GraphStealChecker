def main():
    distances = {
        'F': {'A': 5, 'E': 2, 'C': 16},
        'E': {'A': 12, 'D': 1, 'C': 1, 'F': 2},
        'C': {'E': 1, 'G': 2, 'F': 16},
        'A': {'B': 5, 'D': 3, 'E': 12, 'F': 5},
        'D': {'G': 1, 'E': 1, 'B': 1, 'A': 3},
        'G': {'B': 2, 'D': 1, 'C': 2},
        'B': { 'D': 1, 'A': 5,'G': 2}}
    nodes = ('D', 'E', 'F', 'A', 'B', 'C', 'G')
    print(dijkstra(nodes, distances, 'B'))


def dijkstra(nodes, distances, current):
    current_distance = 0
    visited = {}
    unvisited = {node: None for node in nodes}
    unvisited[current] = current_distance

    while True:
        for neighbour, distance in distances[current].items():
            if neighbour not in unvisited:
                continue
            new_distance = distance + current_distance
            if unvisited[neighbour] is None or unvisited[neighbour] > new_distance:
                unvisited[neighbour] = new_distance
        del unvisited[current]
        visited[current] = current_distance
        if not unvisited:
            break
        candidates = [node for node in unvisited.items() if node[1]]
        current, current_distance = sorted(candidates, key=lambda x: x[1])[0]

    return visited


if __name__ == "__main__":
    main()
