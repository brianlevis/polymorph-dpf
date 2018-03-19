from simulator import *


class DefaultSimulator(Simulator):

    def calculate_price_floor(self, input_features):
        return DEFAULT_FLOOR

    def process_line(self, line, input_features, bids):
        pass


class NaiveSimulator(Simulator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from collections import deque
        self.most_recent_bids = deque([0, 0, 0, 0, 0], maxlen=5)

    def calculate_price_floor(self, input_features):
        return 0.75 * sum(self.most_recent_bids) / self.most_recent_bids.maxlen

    def process_line(self, line, input_features, bids):
        if len(bids) > 0:
            self.most_recent_bids.append(bids[0])


default_simulator = DefaultSimulator(stop=(11, 0), limit=10, delete=False)
naive_simulator = NaiveSimulator(stop=(11, 0), limit=10, download=False)

default_simulator.run_simulation()
naive_simulator.run_simulation()
