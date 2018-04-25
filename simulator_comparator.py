from gametheory import AverageSimulateBid
from simulator import *


class NoFloor(Simulator):
    """Represents no price floor."""

    def calculate_price_floor(self, input_features):
        return 0

    def process_line(self, line, input_features, bids):
        pass


class GlobalRunningAverage(Simulator):
    """Represents a simple running average floor."""

    def __init__(self, *args, history_len=25, weight=0.45, **kwargs):
        super().__init__(*args, **kwargs)
        from collections import deque
        self.most_recent_bids = deque([0] * history_len, maxlen=history_len)
        self.weight = weight

    def calculate_price_floor(self, input_features):
        return self.weight * sum(self.most_recent_bids) / self.most_recent_bids.maxlen

    def process_line(self, line, input_features, bids):
        if len(bids) > 0:
            self.most_recent_bids.append(bids[0])


# tune running average
# for h in range(15, 100, 10):
#     for w in [0.35, 0.375, 0.4, 0.425, 0.45]:
#         queue_simulator(GlobalRunningAverage(history_len=h, weight=w), 'Avg: h=%d, w=%f' % (h, w))
# run_queue(start=(13, 12), stop=(13, 12), limit=15)

# default_simulator = DefaultSimulator(stop=(11, 23))
# naive_simulator_100 = NaiveSimulator(history_len=100)
# naive_simulator_200 = NaiveSimulator(history_len=200)
# oneshot_simulator = MultiShot(10)
# lp_simulator_5 = LinearProgramming(5, 0.000001, 1, 0.1 / 1000)
# lp_simulator_10 = LinearProgramming(10, 0.000001, 1, 0.1 / 1000)
#
# queue_simulator(naive_simulator_100, 'Naive-100')
# queue_simulator(naive_simulator_200, 'Naive-200')
# queue_simulator(oneshot_simulator, 'OneShot')
# queue_simulator(lp_simulator_5, 'LP-5')
queue_simulator(AverageSimulateBid(500, 0.6, 0.3), 'GT (High Revenue)')
queue_simulator(AverageSimulateBid(500, 0.8, 0.2), 'GT (Low Overshoot)')
queue_simulator(GlobalRunningAverage(), 'Basic Running Average')
results = run_queue()


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
