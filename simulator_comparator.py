from simulator import *
from multishot import MultiShot
from gametheory.linear_programming import LinearProgramming


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


# default_simulator = DefaultSimulator(stop=(11, 23))
naive_simulator_100 = NaiveSimulator(history_len=100)
naive_simulator_200 = NaiveSimulator(history_len=200)
oneshot_simulator = MultiShot(10)
lp_simulator_5 = LinearProgramming(5, 0.000001, 1, 0.1 / 1000)
lp_simulator_10 = LinearProgramming(10, 0.000001, 1, 0.1 / 1000)

queue_simulator(naive_simulator_100, 'Naive-100')
queue_simulator(naive_simulator_200, 'Naive-200')
queue_simulator(oneshot_simulator, 'OneShot')
queue_simulator(lp_simulator_5, 'LP-5')

run_queue(stop=(11, 0), limit=2)


# oneshot_simulator_site = MultiShot(id='site_id', stop=(11, 23))
# oneshot_simulator_pub = MultiShot(id='pub_network_id', stop=(11, 23))
# RF simulator trains on 20 (out of 15k) random files from the first 4 days
# random_forest_simulator = RandomForestSimulator(start=(15, 23), download=False, delete=True)

# default_simulator.run_simulation()
# naive_simulator.run_simulation()
# oneshot_simulator.run_simulation()
# oneshot_simulator_site.run_simulation()
# oneshot_simulator_pub.run_simulation()
# random_forest_simulator.run_simulation()
