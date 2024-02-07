class Point:
    def __init__(self, num):
        self.number: int = num
        self.links: list[Link] = []

    def __repr__(self):
        return str(self.number)

    def __getitem__(self, item):
        for link in self.links:
            point_numbers = [point.number for point in link.points]
            if item in point_numbers and self.number in point_numbers:
                return link


class Link:
    def __init__(self, weight: float):
        self.pheromone = 0
        self.weight = weight
        self.points = []

    def __repr__(self):
        return f'{self.points[0]} -> {self.points[1]}'


class Graph:
    def __init__(self):
        self.points: list[Point] = []
        self.links: list[Link] = []

    def __getitem__(self, item: int):
        for el in self.points:
            if el.number == item:  
                return el

    def print_pheromones(self,):
        for link in self.links:
            if link.pheromone - 0.2 > 0:
                print(round(link.pheromone, 2), end=' ')
        print('', end='\t\t')

    def link(self, a: int, b: int, weight: float, pheromone: float = None):
        point_a = self[a]
        point_b = self[b]
        link = Link(weight)
        link.points = [point_a, point_b]
        point_a.links.append(link)
        point_b.links.append(link)
        link.pheromone = pheromone if pheromone else 0
        self.links.append(link)

    def load(self, config: dict):
        self.points = [Point(el) for el in config['points']]

        for el in config['links']:
            self.link(
                el['points'][0],
                el['points'][1],
                el['weight'],
                el['pheromone']
            )


def generate_graph_config(n: int):
    from random import randint
    from pprint import pprint
    points = [i + 1 for i in range(n)]
    links = {}
    for a in points:
        for b in points:
            if (a, b) not in links.keys() and (b, a) not in links.keys() and a != b:
                weight = round(randint(1, 50), 4)
                pheromone = 0.2
                links.update({(a, b): (weight, pheromone)})

    config = {
        "points": points,
        "links": [
            {
                "points": list(key),
                "weight": value[0],
                "pheromone": value[1],
            } for key, value in links.items()
        ]
    }

    pprint(config, sort_dicts=False)


if __name__ == "__main__":
    generate_graph_config(20)
