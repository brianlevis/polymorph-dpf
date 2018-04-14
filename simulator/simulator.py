# Created by Brian Levis on 3/17/18
from simulator.utils import *

from abc import ABC, abstractmethod

DEFAULT_FLOOR = 0.1 / 1000

_simulator_queue = {}


class SimulatorStats:

    def __init__(self):
        # TODO: add timer
        self.total_revenue = 0
        self.auction_count = 0
        self.auction_count_non_null = 0
        self.price_floor_hit_count = 0
        self.price_floor_too_high_count = 0

        self.average_revenue = 0
        self.average_revenue_non_null = 0

        self._total_bid_count = 0
        self._total_bid_amount = 0
        self.average_bid_count = 0
        self.average_bid_count_non_null = 0
        self.average_bid_amount = 0
        self.average_bid_amount_non_null = 0

    def process_line(self, bids, input_features, price_floor):
        revenue = calculate_revenue(bids, price_floor)
        self.total_revenue += revenue
        self.auction_count += 1
        if len(bids) > 0:
            self.auction_count_non_null += 1
            if revenue == price_floor:
                self.price_floor_hit_count += 1
            elif revenue == 0:
                self.price_floor_too_high_count += 1
        self._total_bid_count += len(bids)
        self._total_bid_amount += sum(bids)
        self.average_bid_count = self._total_bid_count / self.auction_count
        self.average_bid_amount = self._total_bid_amount / self.auction_count
        if len(bids) > 0:
            self.average_revenue_non_null = self.total_revenue / self.auction_count_non_null
            self.average_revenue = self.total_revenue / self.auction_count
            self.average_bid_count_non_null = self._total_bid_count / self.auction_count_non_null
            self.average_bid_amount_non_null = self._total_bid_amount / self.auction_count_non_null

    def print_stats(self):
        print("Total Revenue:", self.total_revenue)
        print("Auction Count:", self.auction_count)
        print("Auction Count (non-null):", self.auction_count_non_null)
        print("Price Floor Engaged Count:", self.price_floor_hit_count)
        print("Price Floor Too High Count:", self.price_floor_too_high_count)
        print("Average Revenue:", self.average_revenue)
        print("Average Revenue (not-null):", self.average_revenue_non_null)
        print("Average Bid Count:", self.average_bid_count)
        print("Average Bid Count (non-null):", self.average_bid_count_non_null)
        print("Average Bid Amount:", self.average_bid_amount)
        print("Average Bid Amount (non-null):", self.average_bid_amount_non_null)


class Simulator(ABC):

    def __init__(self, start=(11, 0), stop=(15, 23), limit=None, download=True, delete=True):
        """
        :param start: (day, hour), inclusive
        :param stop: (day, hour), inclusive
        :param limit: maximum number of files to download
        :param download: download data files before simulation
        :param delete: download data files before simulation
        """
        self.start = start
        self.stop = stop
        self.limit = limit
        self.stats = SimulatorStats()
        self.download = download
        self.delete = delete

    @abstractmethod
    def calculate_price_floor(self, input_features):
        pass

    @abstractmethod
    def process_line(self, line, input_features, bids):
        pass

    def run_simulation(self, output='normal'):
        line_iterator = get_line_iterator(start=self.start, stop=self.stop, limit=self.limit, download=self.download,
                                          delete=self.delete)
        for line in line_iterator:
            prepared_line = prepare_line(line)
            bids, input_features = prepared_line['bids'], prepared_line['input_features']
            price_floor = self.calculate_price_floor(input_features)
            self.stats.process_line(bids, input_features, price_floor)
            self.process_line(line, input_features, bids)
        if output != 'none':
            self.stats.print_stats()


def queue_simulator(sim, name):
    """
    :param sim: Simulator object to queue
    :param name: name to be printed with stats
    """
    _simulator_queue[name] = sim


def run_queue(*args, **kwargs):
    stable_queue = _simulator_queue.copy()
    _simulator_queue.clear()
    line_iterator = get_line_iterator(*args, **kwargs)
    for line in line_iterator:
        prepared_line = prepare_line(line)
        bids, input_features = prepared_line['bids'], prepared_line['input_features']
        for sim in stable_queue.values():
            price_floor = sim.calculate_price_floor(input_features)
            sim.stats.process_line(bids, input_features, price_floor)
            sim.process_line(line, input_features, bids)
    for sim in stable_queue:
        print("-------------------------------------------")
        print(sim)
        print("-------------------------------------------")
        stable_queue[sim].stats.print_stats()

# class DefaultSimulator(Simulator):
#
#     def calculate_price_floor(self, input_features):
#         return DEFAULT_FLOOR
#
#     def process_line(self, line, input_features, bids):
#         pass
#
#
# class NaiveSimulator(Simulator):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(self, *args, **kwargs)
#         from collections import deque
#         self.most_recent_bids = deque([0, 0, 0, 0, 0], maxlen=5)
#
#     def calculate_price_floor(self, input_features):
#         return 0.75 * sum(self.most_recent_bids) / self.most_recent_bids.maxlen
#
#     def process_line(self, line, input_features, bids):
#         if len(bids) > 0:
#             self.most_recent_bids.append(bids[0])
