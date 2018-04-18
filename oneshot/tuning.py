import sys
sys.path.append('../') # <- uncomment this if you don't have simulator in your path
from multishot import MultiShot
from simulator import queue_simulator, run_queue

min_over = 100
hyper_h = 0
hyper_e = 0
hyper_l = 0

for h in range(10, 50, 10):
    for e in range(10, 50, 10):
        for l in range(10, 50, 10):
            print("h: " + str(0.01 * h), " e: " + str(0.01 * e) + " l: " + str(0.01 * l))
            oneshot_args = {'price_floor': 0.0002, 'eps': 1.0, 'lamb_h': 0.01 * h, 'lamb_e': 0.01 * e, 'lamb_l': 0.01 * l, 'time': 0, 'M': 5}
            oneshot = MultiShot(1, oneshot_args=oneshot_args)
            queue_simulator(oneshot, "Multishot: (h=%d, e=%d, l=%d)" % (h, e, l))

results = run_queue(output='none')  # <- take away the 'none' too print stats

index = 0
for h in range(10, 50, 10):
    for e in range(10, 50, 10):
        for l in range(10, 50, 10):
            stats = results[index][1].stats
            over_percent = stats.price_floor_too_high_count / stats.auction_count_non_null
            if over_percent < min_over:
                min_over = over_percent
                hyper_h = 0.01 * h
                hyper_e = 0.01 * e
                hyper_l = 0.01 * l
            index += 1

# print("best h: " + str(0.01 * h), " best e: " + str(0.01 * e) + " best l: " + str(0.01 * l))
print("best h: %f best e: %f best l: %f" % (hyper_h, hyper_e, hyper_l))
# Output: best h: 0.100000 best e: 0.100000 best l: 0.100000
# ^ run on a single file
