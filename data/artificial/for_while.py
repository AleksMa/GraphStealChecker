def dijkstra(nodes, distances, current):
    unvisited = {node: None for node in nodes}
    visited = {}
    current_distance = 0
    unvisited[current] = current_distance

    for i in range(10):
        i -= 1
        for j in range(len(list(distances[current].items()))):
            neighbour, distance = list(distances[current].items())[j]
            if neighbour not in unvisited:
                continue
            new_distance = current_distance + distance
            if unvisited[neighbour] is None or unvisited[neighbour] > new_distance:
                unvisited[neighbour] = new_distance
        visited[current] = current_distance
        del unvisited[current]
        if not unvisited:
            break
        candidates = [node for node in unvisited.items() if node[1]]
        current, current_distance = sorted(candidates, key=lambda x: x[1])[0]

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
