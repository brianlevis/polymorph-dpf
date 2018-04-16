import simulator
import itertools
import collections
import numpy as np
from scipy import optimize


class LinearProgramming(simulator.Simulator):
    def __init__(self, memory, delta, discount, default, *args, **kwargs):
        """
        :param memory: (int) the number of previous bids to remember; the space
            complexity of this algorithm is roughly O(memory ** 2)
        :param delta: (double) specifies the aggressiveness of the linear
            approximation; for small deltas, note arithmetic is done on numbers
            with bits on the order of lg(1 / delta)
        :param discount: (double) a parameter which specifies the amount of
            underestimation over the optimal price floor calculated
        :param default: (double) the default price floor to output, given not
            enough information
        """
        super().__init__(*args, **kwargs)
        self.memory = memory
        self.tolerance = 1 / delta
        self.discount = discount
        self.default = default

        self.objective = self._create_objective(memory)
        self.bounds = self._create_bounds(memory)
        self.matrix = self._create_matrix(memory, self.tolerance)

        self.upper = np.zeros(3 * memory)
        self.highs = collections.deque()

    def calculate_price_floor(self, input_features):
        """
        :param input_features: {str: obj} provided feature information
        :return: (float) the price floor to set
        """
        if len(self.highs) < self.memory:
            return self.default

        self._fill_upper_bound()
        results = optimize.linprog(
            self.objective,
            self.matrix,
            self.upper,
            bounds=self.bounds
        )
        if results.success:
            return results.x[0] * self.discount
        return self.default

    def process_line(self, line, input_features, bids):
        """
        :param line: {str: obj} provided line information
        :param input_features: {str: obj} provided feature information
        :param bids: [float] bids given during auction
        :return:
        """
        if not bids:
            return
        highest = sorted(bids, reverse=True)[0]
        self.highs.append(highest)
        if len(self.highs) > self.memory:
            self.highs.popleft()

    def _fill_upper_bound(self):
        """
        :return: (None) updates the upper bound vector to encode the bounds set
            by the bids kept track of by self.highs deque; note that this only
            uses a fixed number more most recent bids, set by the self.memory
            attribute
        """
        for pos, bid in enumerate(self.highs):
            self.upper[3 * pos] = bid * (1 + self.tolerance)

    @staticmethod
    def _create_objective(size):
        """
        :param size: (int) the number of previous bids to keep track of
        :return: [int] a numpy array which encodes the linear objective function
            of the optimization problem
        """
        dimension = 2 * size + 1
        objective = np.ones(dimension)
        objective[0] = 0
        return objective

    @staticmethod
    def _create_bounds(size):
        """
        :param size: (int) the number of previous bids to keep track of
        :return: [()] a list of the variable bounds for the each variable
        """
        bounds = [(0, None)]
        pattern = [(None, None), (0, None)]
        for additional in itertools.repeat(pattern, size):
            bounds.extend(additional)
        return bounds

    @staticmethod
    def _create_matrix(size, tolerance):
        """
        :param size: (int) the number of previous bids to keep track of
        :param tolerance: (float) the aggressiveness of the linear approximation
        :return: [[float]] a numpy array representing the linear constraints of
            the optimization problem
        """
        variables = 2 * size + 1
        constraints = size * 3
        matrix = np.zeros((constraints, variables))

        for block in range(size):
            leading_row, leading_col = 3 * block, 2 * block + 1
            matrix[leading_row][0] = tolerance
            matrix[leading_row + 1][0] = 1
            matrix[leading_row][leading_col] = 1
            matrix[leading_row + 1][leading_col] = 1
            matrix[leading_row + 2][leading_col] = -1
            matrix[leading_row + 2][leading_col + 1] = -1
        return matrix


if __name__ == '__main__':
    settings = [5, 0.000001, 1, 0.1 / 1000]
    test = LinearProgramming(*settings, limit=1, download=False, delete=False)
    test.run_simulation()
