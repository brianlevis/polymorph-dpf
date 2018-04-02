from randomForestSimulator import RandomForestSimulator
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

# import dpf
# from random import randint
#
#
# class MultiShot:
#     # oneshots[0] holds sites w/ returns from init_return to init_return+init_gap
#     # oneshots[1] similarly for init_return+init_gap to init_return+2*init_gap
#     def __init__(self, num_shots, init_return=0.0, init_gap=.05):
#         self.num_shots = num_shots
#         self.init_return = init_return
#         self.init_gap = init_gap
#         self.oneshots = [dpf.DynamicPriceFloor() for _ in range(num_shots)]
#         self.ids = {}  # id -> index of one shot algo
#
#     def get_price_floor(self, input_features):
#         site_id, num_bids = input_features['site_id'], len(input_features['bid_requests'])
#         if site_id not in self.ids:
#             # can also try using average return instead of random
#             oneshot = self.oneshots[randint(0, self.num_shots - 1)]
#             pf = oneshot.get_price_floor(num_bids)
#             idx = (pf + self.init_return) // self.init_gap
#             self.ids[site_id] = idx
#         else:
#             pf = self.oneshots[self.ids[site_id]].get_price_floor(num_bids)
#         self.pf = pf
#         return pf
#
#     def update(self, input_features):
#         bids = input_features['bid_requests']
#         if  in self.ids and hasattr(self, 'pf'):
#             self.oneshots[self.ids[site_id]].update(bids, self.pf)

# Test simulators on the last hour of data
default_simulator = DefaultSimulator(start=(15, 23), download=True, delete=False)
naive_simulator = NaiveSimulator(start=(15, 23), download=False, delete=False)
# RF simulator trains on 20 (out of 15k) random files from the first 4 days
random_forest_simulator = RandomForestSimulator(start=(15, 23), download=False, delete=True)

default_simulator.run_simulation()
naive_simulator.run_simulation()
random_forest_simulator.run_simulation()
