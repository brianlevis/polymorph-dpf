import socket

from gametheory import AverageSingleID
from oneshot import MultiShot
from running_average.running_average import *


# --- Test All ---
# Running average
from vwprediction.simulate import VWSimulator

queue_simulator(RunningAverageWithoutZeros(), "Running Average Without Zeros")
queue_simulator(RunningAverageWithZeros(), "Running Average With Zeros")
queue_simulator(BucketedRunningAverageWithoutZeros(), "Bucketed Running Average Without Zeros")
queue_simulator(BucketedRunningAverageWithZeros(), "Bucketed Running Average With Zeros")

# Weighted Running average
queue_simulator(AverageSingleID(500, 0.6, 0.3, "site_id"), 'GT (High Revenue)')

# OneShot
oneshot_args = {'price_floor': 0.0002, 'eps': 1.0, 'lamb_h': 0.02, 'lamb_e': 0.9, 'lamb_l': 0.88, 'time': 0}
queue_simulator(MultiShot(84, oneshot_args=oneshot_args), 'MultiShot with 84 Buckets')

# Vowpal Wabbit
socket_num = 12345
model_name = '~/polymorph-dpf/vwprediction/models/1_pass'
multiplier = 3.0
os.system("pkill -9 -f 'vw.*--port {0}'".format(socket_num))
os.system("~/vowpal_wabbit/vowpalwabbit/vw --daemon --port {0} --quiet -i {1}.model -t --num_children 1".format(socket_num, model_name))
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', socket_num))
queue_simulator(VWSimulator(sock, multiplier), 'VW (Multiplier: {0})'.format(multiplier))

# Run all in parallel
results = run_queue(start=(14, 0), limit=5) # remove limit to run on all files. See the docstring of this function for details!

os.system("pkill -9 -f 'vw.*--port {0}'".format(socket_num))
