from randomForestSimulator import RandomForestSimulator
from oneshot.dpf import OneShotSimulator
from simulator import *


class DefaultSimulator(Simulator):
    """Represents a static, universal price floor. Note that Polymorph has a default floor of $0.10 CPM,
    but not a universal floor. """

    def calculate_price_floor(self, input_features):
        return DEFAULT_FLOOR

    def process_line(self, line, input_features, bids):
        pass


class NaiveSimulator(Simulator):
    """Represents a simple running average floor."""

    def __init__(self, *args, history_len=5, **kwargs):
        super().__init__(*args, **kwargs)
        from collections import deque
        self.most_recent_bids = deque([0] * history_len, maxlen=history_len)

    def calculate_price_floor(self, input_features):
        return 0.75 * sum(self.most_recent_bids) / self.most_recent_bids.maxlen

    def process_line(self, line, input_features, bids):
        if len(bids) > 0:
            self.most_recent_bids.append(bids[0])


# Test simulators on the last hour of data
default_simulator = DefaultSimulator(start=(15, 23), download=True, delete=False)
naive_simulator = NaiveSimulator(start=(15, 23), download=False, delete=False)
oneshot_simulator = OneShotSimulator(start=(15, 23), download=False, delete=False)
# RF simulator trains on 20 (out of 15k) random files from the first 4 days
random_forest_simulator = RandomForestSimulator(start=(15, 23), download=False, delete=True)

default_simulator.run_simulation()
naive_simulator.run_simulation()
oneshot_simulator.run_simulation()
random_forest_simulator.run_simulation()
