import math
import random

from graph import *
from config import *


def generate_initial_path(graph: Graph):
    path = [el.number for el in graph.points]
    random.shuffle(path)
    path = [*path, path[0]]
    return path


def swap_path_elements(path: list):
    path = [*path]

    a1, a2 = 0, 0
    while a1 == a2:
        a1, a2 = random.randint(1, len(path) - 2), random.randint(1, len(path) - 2)

    a1, a2 = (a2, a1) if a1 > a2 else (a1, a2)

    path[a1], path[a2] = path[a2], path[a1]
    return path


if __name__ == "__main__":
    graph = Graph()
    graph.load(test_graph1)

    current_path = generate_initial_path(graph)
    print(f'{current_path=}')

    t_current = Config.t_max
    min_length = 10000
    i = 0
    while t_current > Config.t_min:
        i += 1
        current_length = graph.length(current_path)
        mutated_path = swap_path_elements(current_path)
        mutated_length = graph.length(mutated_path)

        case = -1
        p = None
        if mutated_length < current_length:
            current_path = mutated_path
            case = 0
        else:
            delta_length = mutated_length - current_length
            p = math.e ** (-delta_length/t_current)
            if random.random() < p:
                current_path = mutated_path
                case = 2
            else:
                case = 1

        t_current *= Config.alpha
        min_length = current_length if current_length < min_length else min_length
        print(f'[{i:8}] -> {t_current=:.2f}, {current_path=} length: current={current_length:.2f} min={min_length:.2f}')
        
