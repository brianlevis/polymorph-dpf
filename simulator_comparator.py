from running_average.running_average import *

# Run comparison


# # --- Tune running average ---
# for w in range(8, 11, 1):
#     for h in range(5, 25, 5):
#         queue_simulator(BucketedRunningAverageWithZeros(history_len=h, weight=w/10.0), 'Bucketed Without Average Avg: h=%d, w=%f' % (h, w/10.0))
# run_queue(limit=2)

#6:58 00-07
queue_simulator(RunningAverageWithoutZeros(), "Running Average Without Zeros")
queue_simulator(RunningAverageWithZeros(), "Running Average With Zeros")
queue_simulator(BucketedRunningAverageWithoutZeros(), "Bucketed Running Average Without Zeros")
queue_simulator(BucketedRunningAverageWithZeros(), "Bucketed Running Average With Zeros")
results = run_queue(start=(14, 0), download=False, delete=False)


# default_simulator = DefaultSimulator(stop=(11, 23))
# naive_simulator_100 = NaiveSimulator(history_len=100)
# naive_simulator_200 = NaiveSimulator(history_len=200)
# oneshot_simulator = MultiShot(10)
# lp_simulator_5 = LinearProgramming(5, 0.000001, 1, 0.1 / 1000)
# lp_simulator_10 = LinearProgramming(10, 0.000001, 1, 0.1 / 1000)


# --- Test All ---
# Running average
# queue_simulator(AverageSingleID(500, 0.6, 0.3, "site_id"), 'GT (High Revenue)')
#
# oneshot_args = {'price_floor': 0.0002, 'eps': 1.0, 'lamb_h': 0.02, 'lamb_e': 0.9, 'lamb_l': 0.88, 'time': 0, 'M': 5}
# queue_simulator(MultiShot(84, oneshot_args=oneshot_args), 'MultiShot with 84 Buckets')
#
# socket_num = 12345
# model_name = '~/polymorph-dpf/vwprediction/models/1_pass'
# multiplier = 3.0
# os.system("pkill -9 -f 'vw.*--port {0}'".format(socket_num))
# os.system("~/vowpal_wabbit/vowpalwabbit/vw --daemon --port {0} --quiet -i {1}.model -t --num_children 1".format(socket_num, model_name))
# socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
# socket.connect(('localhost', socket_num))
# queue_simulator(VWSimulator(socket, multiplier), 'VW (Multiplier: {0})'.format(multiplier))
#
# queue_simulator(RunningAverageWithoutZeros(), 'Basic Running Average of Top Bids')
# # queue_simulator(RunningAverageWithBuckets(), 'Running Average by site_id')
# # queue_simulator(RunningAverageWithBuckets(feature='pub_network_id'), 'Running Average by pub_network_id')
#
# results = run_queue(start=(14, 0))
#
# os.system("pkill -9 -f 'vw.*--port {0}'".format(socket_num))
