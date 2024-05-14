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

    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def forward(self, X):
        # Forward pass
        self.activations = [X]
        for i in range(self.num_layers - 1):
            layer_input = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            layer_output = self.sigmoid(layer_input)
            self.activations.append(layer_output)
        return self.activations[-1]

    def backward(self, X, y, learning_rate):
        # Backpropagation
        errors = [None] * (self.num_layers - 1)
        deltas = [None] * (self.num_layers - 1)

        errors[-1] = y - self.activations[-1]
        deltas[-1] = errors[-1] * self.sigmoid_derivative(self.activations[-1])

        for i in range(self.num_layers - 2, 0, -1):
            errors[i - 1] = deltas[i].dot(self.weights[i].T)
            deltas[i - 1] = errors[i - 1] * self.sigmoid_derivative(self.activations[i])

        # Update weights and biases
        for i in range(self.num_layers - 1):
            self.weights[i] += self.activations[i].T.dot(deltas[i]) * learning_rate
            self.biases[i] += np.sum(deltas[i], axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, learning_rate)
            if epoch % int(epochs / 10) == 0:
                loss = np.mean(np.square(y - output))
                print(f"Epoch {epoch}, Loss: {loss}")


def sum_cases():
    get_values = lambda: (random.randint(0, 3) / 3 for _ in range(3))
    learn_cases = set()
    while len(learn_cases) < 50:
        a, b, c = get_values()
        value = (
            (a, b, c),
            int(sum([a, b, c]) * 3 % 2)
        )

        learn_cases.add(value)

    check_cases = set()
    while len(check_cases) < 14:
        a, b, c = get_values()
        value = (
            (a, b, c),
            int(sum([a, b, c]) * 3 % 2)
        )
        if value not in learn_cases:
            check_cases.add(value)

    learn_x, learn_y = [list(el[0]) for el in learn_cases], [[el[1]] for el in learn_cases]
    check_x, check_y = [list(el[0]) for el in check_cases], [[el[1]] for el in check_cases]

    return learn_x, learn_y, check_x, check_y


# Example usage
if __name__ == "__main__":
    learn_x, learn_y, check_x, check_y = sum_cases()

    layer_config = [3, 5, 10, 5, 1]  # Number of neurons in each layer

    nn = NeuralNetwork(layer_config)
    nn.train(np.array(learn_x), np.array(learn_y), epochs=100_000, learning_rate=0.1)
    print("Final predictions:")

    count = 0
    for initial, res, expect in zip(check_x, nn.forward(np.array(check_x)), check_y):
        initial = [int(el*3) for el in initial]
        print(initial, res, expect, end=' ')
        res = round(res[0]) == expect[0]
        count += 1 if res else 0
        print(res)

    print(F'total: {count}/{len(check_y)}')
