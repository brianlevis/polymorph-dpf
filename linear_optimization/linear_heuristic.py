import simulator
import itertools
import numpy as np
from scipy import optimize


class LinearHeuristic(simulator.Simulator):
    """
    An linear programming approach to direct revenue optimization. (Currently
    does not work.)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate_price_floor(self, input_features):
        """
        :param input_features: {str: obj} provided feature information
        :return: (float) the price floor to set
        """
        pass

    def process_line(self, line, input_features, bids):
        """
        :param line: {str: obj} provided line information
        :param input_features: {str: obj} provided feature information
        :param bids: [float] bids given during auction
        :return:
        """
        pass


if __name__ == '__main__':
    pass
