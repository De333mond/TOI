import numpy as np
import pickle


class Network:

    @staticmethod
    def sigmoid(input: np.array):
        return np.array([])

    def __init__(self, layers: list[int], func: callable):
        self.layers = layers
        self.weights = []
        self.b_list = []

        self.func = func

        try:
            self.load()
        except FileNotFoundError:
            self.create_random()


    def create_random(self):
        prev = None
        for curr in self.layers:
            if prev:
                self.weights.append(np.random.randn(prev, curr))
                self.b_list.append(np.random.randn(curr))
            prev = curr


    def calculate(self, input: np.array):
        for i, weight in enumerate(self.weights):
            input = self.func(input @ weight + self.b_list[i])
        return input

    def save(self):
        title = '-'.join([str(el) for el in self.layers])
        with open(f'networks/{title}.pickle', 'wb') as file:
            pickle.dump(self.__dict__, file)

    def load(self, ):
        title = '-'.join([str(el) for el in self.layers])
        with open(f'networks/{title}.pickle', 'rb') as file:
            self.__dict__ = pickle.load(file)


if __name__ == "__main__":
    network = Network([2, 3, 2])

    network.save()
    print(network.__dict__)
