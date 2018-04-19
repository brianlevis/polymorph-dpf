import sys
sys.path.append('../')

from simulator import *
from gametheory import Average, AverageBidderID, AverageSingleID

test_windows = [50, 100, 250, 500, 1000]
test_weights = [x / 10.0 for x in range(0, 11, 1)]
test_bidder_id_weights = [x / 10.0 for x in range(0, 11, 1)]

default_start = (11, 0)
default_stop = (11, 2)
default_limit = 100

def download():
    """
    Dummy run to download all files for the first time
    """
    download = Average(1, 0.5, start=default_start, stop=default_stop, limit=default_limit, download=True, delete=False)
    download.run_simulation()

def tuneAverage(windows=test_windows, weights=test_weights):
    """
    :param windows: list of window values to test
    :param weights: list of weight values to test
    :param output: dict to modify to save progress in case of crash
    """
    for window in windows:
        for weight in weights:
            sim = Average(window, weight, start=default_start, stop=default_stop, limit=default_limit, download=False, delete=False)
            name = "Average : window={}, weight={}".format(window, weight)
            queue_simulator(sim, name)
    
    output = run_queue(output='none')
    return output

def tuneAverageBidderID(windows=test_windows, weights=test_bidder_id_weights):
    """
    :param windows: list of window values to test
    :param weights: list of bidder weight values to test
    :param output: dict to modify to save progress in case of crash

    Note that weight is used differently for AverageBidderID!
    """
    for window in windows:
        for weight in weights:
            sim = AverageBidderID(window, weight, start=default_start, stop=default_stop, limit=default_limit, download=False, delete=False)
            name = "AverageBidderID : window={}, weight={}".format(window, weight)
            queue_simulator(sim, name)
    
    output = run_queue(output='none')
    return output

def tuneAverageSingleID(windows=test_windows, weights=test_weights, param_id=None):
    """
    :param windows: list of window values to test
    :param weights: list of weight values to test
    :param param_id: string name of a single-value input feature (e.g. site_id, pub_network_id)
    :param output: dict to modify to save progress in case of crash
    """
    for window in windows:
        for weight in weights:
            sim = AverageSingleID(window, weight, param_id, start=default_start, stop=default_stop, limit=default_limit, download=False, delete=False)
            name = "AverageBidderID : param_id={}, window={}, weight={}".format(param_id, window, weight)
            queue_simulator(sim, name)
    
    output = run_queue(output='none')
    return output

# def printPrettyStats(stats):
#     # print("-------------------------------------------")
#     # print()
#     # print("-------------------------------------------")
#     for k in stats:
#         if k == "price_floor_hit_percent" or k == "price_floor_too_high_percent":
#             print("{}: {:.2%}".format(k, stats[k]))
#         else:
#             print("{}: {}".format(k, stats[k]))

# def getStats(sim):
#     stats = {}

#     stats["timer"] = sim.timer
#     stats["total_revenue"] = sim.total_revenue
#     stats["auction_count"] = sim.auction_count
#     stats["auction_count_non_null"] = sim.auction_count_non_null
#     stats["price_floor_hit_count"] = sim.price_floor_hit_count
#     stats["price_floor_too_high_count"] = sim.price_floor_too_high_count

#     stats["price_floor_hit_percent"] = sim.price_floor_hit_count / sim.auction_count_non_null
#     stats["price_floor_too_high_percent"] = sim.price_floor_too_high_count / sim.auction_count_non_null

#     stats["average_revenue"] = sim.average_revenue
#     stats["average_revenue_non_null"] = sim.average_revenue_non_null

#     stats["total_bid_count"] = sim._total_bid_count
#     stats["total_bid_amount"] = sim._total_bid_amount
#     stats["average_bid_count"] = sim.average_bid_count
#     stats["average_bid_count_non_null"] = sim.average_bid_count_non_null
#     stats["average_bid_amount"] = sim.average_bid_amount
#     stats["average_bid_amount_non_null"] = sim.average_bid_amount_non_null

#     return stats