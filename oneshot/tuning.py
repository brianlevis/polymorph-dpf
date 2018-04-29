import sys
sys.path.append('../') # <- uncomment this if you don't have simulator in your path
from multishot import MultiShot
from simulator import queue_simulator, run_queue
import numpy as np

min_over = 100
max_revenue = 0
over_hyper_h = 0
over_hyper_e = 0
over_hyper_l = 0

lambda_min = 0.1
lambda_max = 0.9
range_step = 5
range_min = int(lambda_min * 100)
range_max = int(lambda_max * 100)

for h in range(range_min, range_max, range_step):
    for e in range(range_min, range_max, range_step):
        for l in range(range_min, range_max, range_step):
            print("h: " + str(0.01 * h), " e: " + str(0.01 * e) + " l: " + str(0.01 * l))
            oneshot_args = {'price_floor': 0.0002, 'eps': 1.0, 'lamb_h': 0.01 * h, 'lamb_e': 0.01 * e, 'lamb_l': 0.01 * l, 'time': 0, 'M': 5}
            oneshot = MultiShot(1, oneshot_args=oneshot_args, limit=3)
            queue_simulator(oneshot, "Multishot (1 bucket): (h=%.2f, e=%.2f, l=%.2f)" % (0.01 * h, 0.01 * e, 0.01 * l))
            oneshot = MultiShot(2, oneshot_args=oneshot_args, limit=3)
            queue_simulator(oneshot, "Multishot (2 buckets): (h=%.2f, e=%.2f, l=%.2f)" % (0.01 * h, 0.01 * e, 0.01 * l))

# for i in range(1, 10):
#     oneshot_args = {}
#     oneshot = MultiShot(i, oneshot_args=oneshot_args, limit=3)
#     queue_simulator(oneshot, "Multishot: %d buckets" % (i))

results = run_queue(limit=5)  # <- take away the 'none' too print stats

index = 0
for h in range(range_min, range_max, range_step):
    for e in range(range_min, range_max, range_step):
        for l in range(range_min, range_max, range_step):
            stats = results[index][1].stats
            over_percent = 100 * stats.price_floor_too_high_count / stats.auction_count_non_null
            revenue = stats.total_revenue
            if over_percent < min_over:
                min_over = over_percent
                over_hyper_h = 0.01 * h
                over_hyper_e = 0.01 * e
                over_hyper_l = 0.01 * l
            if revenue > max_revenue:
                max_revenue = revenue
                revenue_hyper_h = 0.01 * h
                revenue_hyper_e = 0.01 * e
                revenue_hyper_l = 0.01 * l
            index += 1

            # one_shot = oneshot.oneshots[0]
            # print(one_shot.log)
            # max_bids, overshoots = one_shot.max_bid, one_shot.over
            # max_bids, overshoots = np.array(max_bids), np.array(overshoots)
            # print(np.max(max_bids), np.max(overshoots))
            # print(np.max(max_bids - overshoots))


# print("best h: " + str(0.01 * h), " best e: " + str(0.01 * e) + " best l: " + str(0.01 * l))
print("overshooting best h: %f best e: %f best l: %f" % (over_hyper_h, over_hyper_e, over_hyper_l))
print("revenue best h: %f best e: %f best l: %f" % (revenue_hyper_h, revenue_hyper_e, revenue_hyper_l))
