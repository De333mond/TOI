import numpy as np
from typing import Callable


class Funcs:
    relu = lambda x: np.maximum(x, 0)
    softmax = lambda x: np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)

    @staticmethod
    def stable_softmax(x):
        exps = np.exp(x - np.max(x, axis=1, keepdims=True))
        return exps / np.sum(exps, axis=1, keepdims=True)

    sigmoid = lambda x: 1 / (1 + np.exp(-x))
    sigmoid_derivative = lambda x: x * (1 - x)

class NeuralNetwork:
    def __init__(self, layer_config, activator: Callable, out_func: Callable | None = None):
        self.activator = activator
        self.out_func = out_func
        self.layer_config = layer_config
        self.num_layers = len(layer_config)

        # Initialize weights and biases
        self.weights = [np.random.randn(layer_config[i], layer_config[i + 1]) for i in range(self.num_layers - 1)]
        self.biases = [np.zeros((1, layer_config[i + 1])) for i in range(self.num_layers - 1)]

    @staticmethod
    def Relu(x):
        return

    def forward(self, X):
        self.activations = [X]
        for i in range(self.num_layers - 1):
            layer_input = np.dot(self.activations[-1], self.weights[i]) + self.biases[i]
            output_layer = self.activator(layer_input)
            self.activations.append(output_layer)

        return self.out_func(self.activations[-1]) if self.out_func else self.activations[-1]

# Example usage


class BackProp(NeuralNetwork):
    def backward(self, X, y, learning_rate, back_func):
        # Backpropagation
        error = y - self.predicted_output
        d_predicted_output = error * self.sigmoid_derivative(self.predicted_output)

        error_hidden = d_predicted_output.dot(self.weights_hidden_output.T)
        d_hidden_output = error_hidden * self.sigmoid_derivative(self.hidden_output)

        # Update weights and biases
        self.weights_hidden_output += self.hidden_output.T.dot(d_predicted_output) * learning_rate
        self.bias_hidden_output += np.sum(d_predicted_output, axis=0, keepdims=True) * learning_rate
        self.weights_input_hidden += X.T.dot(d_hidden_output) * learning_rate
        self.bias_input_hidden += np.sum(d_hidden_output, axis=0, keepdims=True) * learning_rate

    def train(self, X, y, epochs, learning_rate, back_func):
        for epoch in range(epochs):
            output = self.forward(X)
            self.backward(X, y, learning_rate, back_func)
            if epoch % 100 == 0:
                loss = np.mean(np.square(y - output))
                print(f"Epoch {epoch}, Loss: {loss}")