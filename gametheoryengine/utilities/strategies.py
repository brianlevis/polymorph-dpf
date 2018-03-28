import collections
import utilities.engine as engine
import numpy as np


class Constant(engine.Strategy):
    """
    A strategy that simply outputs a constant reserve price, which can be set
    during instantiation.
    """
    def __init__(self, default=0):
        """
        :param default: (float) the default reserve price to output
        """
        self.default = default

    def get_reserve(self):
        return self.default

    def update(self, auction_info, bid_prices, previous):
        pass


class GameTheory(engine.Strategy):
    """
    A game theoretic approach to setting the price floor: the object keeps track
    of a fixed number of recent auctions with 2 bidders or more. It then issues
    a reserve price that is in between the average of the second bidder and
    the average of the first.
    """
    def __init__(self, window_length, fraction):
        """
        :param window_length: (int) the number of previous auctions to store at
            one time
        :param fraction: [float] a decimal between 0 and 1 inclusive which
            signifies the distance to the first bid
        """
        self.first_sum = 0
        self.second_sum = 0
        self.fraction = fraction
        self.window_length = window_length
        self.window = collections.deque()

    def get_reserve(self):
        if len(self.window) < self.window_length:
            return 0
        top_mean = self.first_sum / self.window_length
        bottom_mean = self.second_sum / self.window_length
        difference = top_mean - bottom_mean
        return bottom_mean + difference * self.fraction

    def update(self, auction_info, bid_prices, previous):
        if len(bid_prices) < 2:
            return
        self._include(bid_prices[0], bid_prices[1])
        if len(self.window) > self.window_length:
            self._exclude()

    def _include(self, first_bid, second_bid):
        self.first_sum += first_bid
        self.second_sum += second_bid
        self.window.appendleft((first_bid, second_bid))

    def _exclude(self):
        first_bid, second_bid = self.window.pop()
        self.first_sum -= first_bid
        self.second_sum -= second_bid


class BruteForceOptimization(engine.Strategy):
    """
    An optimization approach that simply looks for the best price floor to
    maximize revenue at each time interval. This, indeed, takes a while.
    """
    def __init__(self, window_length, lower, upper, step):
        """
        :param window_length: (int) the number of previous auctions to store at
            one time
        :param lower: (num) the lower bound for values to try
        :param upper: (num) the upper bound, exclusive up to float round-off,
            error, for values to try
        :param step: (num) the distance between consecutive values to try
        """
        self.range = np.arange(lower, upper, step)
        self.window_length = window_length
        self.window = collections.deque()

    def get_reserve(self):
        revenues = [self._calculate_revenue(floor) for floor in self.range]
        max_position = np.argmax(revenues)
        return self.range[max_position]

    def update(self, auction_info, bid_prices, previous):
        if len(bid_prices) == 1:
            self.window.appendleft((1, bid_prices[0]))
        elif len(bid_prices) > 1:
            pair = (2, bid_prices[0], bid_prices[1])
            self.window.appendleft(pair)
        if len(self.window) > self.window_length:
            self.window.pop()

    def _calculate_revenue(self, price_floor):
        total = 0
        for bids in self.window:
            bidders = bids[0]
            if bids[1] >= price_floor and bidders == 1:
                total += bids[1]
            elif bids[1] >= price_floor and bidders == 2:
                sales_price = max(price_floor, bids[2])
                total += sales_price
        return total
