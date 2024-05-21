import random

import numpy as np

np.random.seed(1)


class NeuralNetwork:
    def __init__(self, layer_config):
        self.layer_config = layer_config
        self.num_layers = len(layer_config)

        # Initialize weights and biases
        self.weights = [np.random.randn(layer_config[i], layer_config[i + 1]) for i in range(self.num_layers - 1)]
        self.biases = [np.zeros((1, layer_config[i + 1])) for i in range(self.num_layers - 1)]

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))


    def forward(self, X):
        # Forward pass
        self.activations = [X]
        for i in range(self.num_layers - 1):
            layer_input = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            layer_output = self.sigmoid(layer_input)
            self.activations.append(layer_output)
        return self.activations[-1]

    def change_weight(self, X, a=1.0):
        self.forward(X)

        # Hebbian learning
        for i in range(len(self.weights)):
            input_activations = self.activations[i]
            output_activations = self.activations[i + 1]
            # Update weights based on Hebbian rule
            delta = a * np.dot(input_activations.T, output_activations)

            self.weights[i] += delta



def sum_cases():
    get_values = lambda: (random.random() * 2 - 1 for _ in range(3))

    learn_cases = set()
    while len(learn_cases) < 250:
        a, b, c = get_values()
        value = (
            (a, b, c),
            int(sum([a, b, c]) > 0)
        )

        learn_cases.add(value)

    check_cases = set()
    while len(check_cases) < 20:
        a, b, c = get_values()
        value = (
            (a, b, c),
            int(sum([a, b, c]) > 0.5)
        )
        if value not in learn_cases:
            check_cases.add(value)

    learn_x, learn_y = [list(el[0]) for el in learn_cases], [[el[1]] for el in learn_cases]
    check_x, check_y = [list(el[0]) for el in check_cases], [[el[1]] for el in check_cases]

    return learn_x, learn_y, check_x, check_y


if __name__ == "__main__":
    nw = NeuralNetwork([3, 5, 10, 1, 1])

    learn, _, check, check_res = sum_cases()

    for i in range(10):
        for el in learn:
            nw.change_weight(np.array([el]), a=0.1)

    print("Final predictions:")
    count = 0
    for initial, res, expect in zip(check, nw.forward(np.array(check)), check_res):
        initial = ' ,'.join([f"{el:.3f}" for el in initial])
        initial = f'[{initial}]'
        print(initial, res, expect, end=' ')
        res = round(res[0]) == expect[0]
        count += 1 if res else 0
        print(res)

    print(F'total: {count}/{len(check_res)}')
