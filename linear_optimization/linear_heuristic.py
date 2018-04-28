import simulator
import collections
import numpy as np
import itertools
from scipy import optimize


class LinearHeuristic(simulator.Simulator):
    """
    An linear heuristic to estimate a price floor close to the optimal.
    """

    def __init__(self, memory, up, down, discount, default, *args, **kwargs):
        """
        :param memory: (int) the number of previous bids to remember; the space
            complexity of this algorithm is roughly O(memory ** 2)
        :param up: (float) specifies the slope of the linear function to the
            left of the local optimal, should be positive
        :param down: (float) specifies the slope of the linear function to the
            right of the local optimal, should be negative
        :param discount: (double) a parameter which specifies the amount of
            underestimation over the optimal price floor calculated
        :param default: (double) the default price floor to output, given not
            enough information
        """
        super().__init__(*args, **kwargs)
        self.memory = memory
        self.up_slope = up
        self.down_slope = down
        self.discount = discount
        self.default = default

        self.objective = self._create_objective(memory)
        self.bounds = self._create_bounds(memory)
        self.matrix = self._create_matrix(memory, up, down)
        self.upper = np.zeros(2 * memory)

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
            self.upper[2 * pos] = bid * (1 - self.up_slope)
            self.upper[2 * pos + 1] = bid * (1 - self.down_slope)

    @staticmethod
    def _create_objective(size):
        """
        :param size: (int) the number of previous bids to keep track of
        :return: [int] a numpy array which encodes the linear objective function
            of the optimization problem
        """
        dimension = size + 1
        objective = np.ones(dimension) * -1
        objective[0] = 0
        return objective

    @staticmethod
    def _create_bounds(size):
        """
        :param size: (int) the number of previous bids to keep track of
        :return: [()] a list of the variable bounds for the each variable
        """
        bounds = [(0, None)]
        pattern = itertools.repeat((None, None), size)
        bounds.extend(pattern)
        return bounds

    @staticmethod
    def _create_matrix(size, up_slope, down_slope):
        """
        :param size: (int) the number of previous bids to keep track of
        :param up_slope: (float) specifies the slope of the linear function to
            the left of the local optimal, should be positive
        :param down_slope: (float) specifies the slope of the linear function to
            the right of the local optimal, should be negative
        :return: [[float]] a numpy array representing the linear constraints of
            the optimization problem
        """
        variables = size + 1
        constraints = size * 2
        matrix = np.zeros((constraints, variables))

        for block in range(size):
            leading_row, leading_col = 2 * block, block + 1
            matrix[leading_row][0] = -up_slope
            matrix[leading_row + 1][0] = -down_slope
            matrix[leading_row][leading_col] = 1
            matrix[leading_row + 1][leading_col] = 1
        return matrix


if __name__ == '__main__':
    settings = {
        'memory': 30,
        'up': 1,
        'down': -1.1,
        'discount': 1,
        'default': 0.1 / 1000
    }
    test = LinearHeuristic(**settings, limit=1, download=True, delete=False)
    test.run_simulation()
