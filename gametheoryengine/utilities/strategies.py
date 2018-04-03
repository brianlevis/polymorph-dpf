import collections
import utilities.engine as engine
import numpy as np

RESPONSES_ATTR = 'bid_responses'
ID_ATTR = 'id'
BID_PRICE_ATTR = 'bid_price'


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

    def get_reserve(self, auction_info):
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

    def get_reserve(self, auction_info):
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


class GameTheoryPerID(engine.Strategy):
    """
    Keeps a unique running average for each bidder. For each auction, 
    participating bidders' running averages are averaged together, then
    multiplied by self.fraction to get the reserve price. self.fraction should
    act as a weight (i.e. 0.9 would cause the reserve to undershoot a bit)

    """
    def __init__(self, minimum_length, fraction, attribute_id, static):
        """
        :param minimum_length: (int) the minimum length after which to rely
            on the game theory strategy
        :param fraction: (float) a decimal between 0 and 1 inclusive which
            discounts from the average bid
        :param attribute_id: (str) the attribute to track
        :param static: (float) the default static price floor to output given
            not enough information
        """
        self.static = static
        self.attribute_id = attribute_id
        self.fraction = fraction
        self.minimum_length = minimum_length
        self.averages = {}
        self.counts = {}

    def get_reserve(self, auction_info):
        key = auction_info[self.attribute_id]
        if key not in self.counts or self.counts[key] < self.minimum_length:
            return self.static
        return self.fraction * self.averages[key]

    def update(self, auction_info, bid_prices, previous):
        if not bid_prices:
            return
        key = auction_info[self.attribute_id]
        add_bidders = len(bid_prices)
        add_average = sum(bid_prices) / add_bidders
        if key in self.averages:
            new_count = self.counts[key] + add_bidders
            new_average = self.averages[key] * (1 - add_bidders / new_count) \
                + add_average * add_bidders / new_count
            self.counts[key] = new_count
            self.averages[key] = new_average
        else:
            self.counts[key] = add_bidders
            self.averages[key] = add_average


class BruteForceOptimization(engine.Strategy):
    """
    TODO: Incomplete
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

    def get_reserve(self, auction_info):
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


class LinearOptimization(engine.Strategy):
    """
    TODO: Incomplete
    """
    def __init__(self):
        pass

    def get_reserve(self, auction_info):
        pass

    def update(self, auction_info, bid_prices, previous):
        pass
