import random

from graph import *
from settings import *


def get_weights(point, visited: list):
    point: Point
    weights = {}
    for link in point.links:
        link: Link

        to_point = link.points[1] if link.points[0].number == point.number else link.points[0]
        if to_point in visited:
            continue

        weight = ((link.pheromone ** alpha) * ((1 / link.weight) ** beta))

        s = 0

        for el in point.links:
            to = el.points[1] if el.points[0].number == point.number else el.points[0]
            if to not in visited:
                s += ((el.pheromone ** alpha) * ((1 / el.weight) ** beta))

        weight /= s

        weights.update({to_point: weight})

    return weights


def do_iteration(graph: Graph):

    points_queue = graph.points
    random.shuffle(points_queue)

    paths = []

    for point in points_queue:
        point: Point

        visited = []
        current_point = point
        while len(visited) < len(graph.points) - 1:
            visited.append(current_point)
            weights = get_weights(current_point, visited)

            items = [item[0] for item in weights.items()]
            item_weights = [item[1] for item in weights.items()]

            current_point = random.choices(items, cum_weights=item_weights, k=1)[0]

        visited.append(current_point)
        visited.append(point)
        paths.append(visited)

    return paths


def apply_pheromone_change(paths: list):
    pheromone_deltas = {}

    min_length = 10000000
    min_path = None
    for path in paths:

        length = 0
        for i, el in enumerate(path[1:]):
            length += path[i][el.number].weight

        if length < min_length:
            min_length = length
            min_path = path

        for i, el in enumerate(path[1:]):
            link = path[i][el.number]
            pheromone_delta = Q / length

            if link not in pheromone_deltas.keys():
                pheromone_deltas.update({link: pheromone_delta})
            else:
                pheromone_deltas[link] += pheromone_delta
        # print(f'{length=} {min_length=} ')
        # print(length, end=', ')
    for link in graph.links:
        link.pheromone = (1 - p) * link.pheromone

        if link in pheromone_deltas.keys():
            link.pheromone += pheromone_deltas[link]

        if pheromone_cup and link.pheromone > pheromone_cup:
            link.pheromone = pheromone_cup

    return min_length, min_path


if __name__ == "__main__":
    graph = Graph()
    graph.load(test_graph)

    min_length = 1000

    for i in range(10000):
        # graph.print_pheromones()
        paths = do_iteration(graph)
        length, path = apply_pheromone_change(paths)
        min_length = length if length < min_length else min_length
        print(f'iteration: {i + 1}, {length=} {min_length=} ')

    print('end')
