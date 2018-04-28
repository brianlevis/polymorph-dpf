from gametheory import AverageSimulateBid
from oneshot import MultiShot
from vwprediction.simulate import VWSimulator
from simulator import *

import socket as sock

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

# Run comparison


# --- Tune running average ---
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

# --- Test All ---
queue_simulator(AverageSimulateBid(500, 0.6, 0.3), 'GT (High Revenue)')
queue_simulator(AverageSimulateBid(500, 0.8, 0.2), 'GT (Low Overshoot)')

oneshot_args = {'price_floor': 0.0002, 'eps': 1.0, 'lamb_h': 0.1, 'lamb_e': 0.1, 'lamb_l': 0.1, 'time': 0, 'M': 5}
oneshot_args_no_ceiling = oneshot_args.copy()
oneshot_args_no_ceiling['pf_ceil'] = 0.1
queue_simulator(MultiShot(1, oneshot_args=oneshot_args), 'MultiShot')
queue_simulator(MultiShot(1, oneshot_args=oneshot_args_no_ceiling), 'MultiShot (no ceiling)')

socket_num = 12345
model_name = '~/polymorph-dpf/vwprediction/models/1_pass'
multiplier = 3.0
os.system("pkill -9 -f 'vw.*--port {0}'".format(socket_num))
os.system("~/vowpal_wabbit/vowpalwabbit/vw --daemon --port {0} --quiet -i {1}.model -t --num_children 1".format(socket_num, model_name))
socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
socket.connect(('localhost', socket_num))
queue_simulator(VWSimulator(socket, multiplier), 'VW (Multiplier: {0})'.format(multiplier))

queue_simulator(GlobalRunningAverage(), 'Basic Running Average')
queue_simulator(NoFloor(), 'No Price Floor')

results = run_queue(start=(14, 0))

os.system("pkill -9 -f 'vw.*--port {0}'".format(socket_num))

# --- Test OneShot Bucket distribution
# num_buckets = 20
# oneshot_args = {'price_floor': 0.0002, 'eps': 1.0, 'lamb_h': 0.1, 'lamb_e': 0.1, 'lamb_l': 0.1, 'time': 0, 'M': 5}
# queue_simulator(MultiShot(num_buckets, oneshot_args=oneshot_args), 'Multishot bucket test')
# results = run_queue(limi t=1, delete=False)
# totals = {str(n): 0 for n in range(num_buckets)}
# ids = results[0][1].ids
# for b in ids.values():
#     totals[str(b)] += 1
# print(totals)
