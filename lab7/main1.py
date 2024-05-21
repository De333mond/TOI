import numpy as np


class KohonenSOM:
    def __init__(self, grid_size, input_dim, learning_rate=0.1, radius=1.0, decay=0.99):
        self.grid_size = grid_size
        self.input_dim = input_dim
        self.learning_rate = learning_rate
        self.radius = radius
        self.decay = decay

        # Initialize the weights randomly
        self.weights = np.random.rand(grid_size[0], grid_size[1], input_dim)
        self._init_neighborhood()

    def _init_neighborhood(self):
        """Initialize the neighborhood matrix."""
        self.neighborhood = np.zeros((self.grid_size[0], self.grid_size[1], self.grid_size[0], self.grid_size[1]))
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                for k in range(self.grid_size[0]):
                    for l in range(self.grid_size[1]):
                        self.neighborhood[i, j, k, l] = np.exp(-((i - k) ** 2 + (j - l) ** 2) / (2 * self.radius ** 2))

    def _update_learning_rate(self):
        """Decay the learning rate and radius over time."""
        self.learning_rate *= self.decay
        self.radius *= self.decay
        self._init_neighborhood()

    def _find_bmu(self, x):
        """Find the Best Matching Unit (BMU) for a given input vector."""
        distances = np.linalg.norm(self.weights - x, axis=2)
        bmu_index = np.unravel_index(np.argmin(distances), distances.shape)
        return bmu_index

    def _update_weights(self, x, bmu_index):
        """Update the weights of the SOM."""
        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                influence = self.neighborhood[bmu_index[0], bmu_index[1], i, j]
                self.weights[i, j] += self.learning_rate * influence * (x - self.weights[i, j])

    def train(self, data, num_iterations):
        """Train the SOM on the given data."""
        for iteration in range(num_iterations):
            for x in data:
                bmu_index = self._find_bmu(x)
                self._update_weights(x, bmu_index)
            self._update_learning_rate()
            print(f"Iteration {iteration + 1}/{num_iterations} completed.")

    def map_vects(self, data):
        """Map each input vector to its corresponding BMU in the SOM."""
        mapped = []
        for x in data:
            mapped.append(self._find_bmu(x))
        return mapped


# Example usage
if __name__ == "__main__":
    # Define parameters
    grid_size = (10, 10)  # 10x10 grid
    input_dim = 3  # Input dimension (e.g., 3 for RGB colors)
    learning_rate = 0.1
    radius = 1.0
    decay = 0.99
    num_iterations = 100

    # Generate some random input data
    data = np.random.rand(100, input_dim)

    # Create and train the SOM
    som = KohonenSOM(grid_size, input_dim, learning_rate, radius, decay)
    som.train(data, num_iterations)

    # Map the input vectors to the SOM grid
    mapped = som.map_vects(data)
    print("Mapped vectors:", mapped)
