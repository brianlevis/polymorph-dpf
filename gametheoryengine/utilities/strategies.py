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


class GameTheoryPerID(engine.Strategy):
    """
    Keeps a unique running average for each bidder. For each auction, 
    participating bidders' running averages are averaged together, then
    multiplied by self.fraction to get the reserve price. self.fraction should
    act as a weight (i.e. 0.9 would cause the reserve to undershoot a bit)

    @Hermish: b/c this needs bidder IDs attached to price, you'll need to add
    functions to pass in extra info to params versus your GameTheory class.
    In this case it's easier to just pass in bid_responses unprocessed since
    I don't need to know first/second highest bidder per auction anymore.

    """
    def __init__(self, window_length, fraction):
        """
        :param window_length: (int) the number of previous auctions to store at
            one time
        :param fraction: [float] a decimal between 0 and 1 inclusive which
            signifies the distance to the first bid
        """
        
        self.fraction = fraction
        self.window_length = window_length

        # self.averages holds running avg (float) for each bidder ID key
        # e.g. "12345": 0.000987. Bidder IDs are ints, may have to cast to
        # str for them to be hashable, e.g. self.averages[str(bid['id'])].
        self.averages = {}

    def get_reserve(self, bid_responses):
        """
        (idk how you generate these, sorry bout the formatting)
        bid_responses: the list of dicts from the JSON

        Returns average of participating bidders' individual running avgs (if they
        have bid before/exist in self.averages), multiplied by self.fraction to 
        weight it (e.g. 0.9 to try to undershoot a bit).
        """
        if len(bid_responses) == 0:
            return 0
        
        count = 0
        reserve = 0
        for bid in bid_responses:
            if bid['id'] in self.averages:
                reserve += self.averages[bid['bid_price']]
                count += 1

        if count == 0:
            return 0 # Or return some constant STATIC_RESERVE

        reserve = reserve / count

        return self.fraction * reserve

    def update(self, bid_responses):
        """
        bid_responses: the list of dicts from the JSON

        Moving avg w/out tracking: https://stackoverflow.com/questions/12636613/
        Using implementation from answer #2.
        May want to consider exponential moving average in the future.
        FLAW: earlier bids are weighted way too much until we start getting 
        close to window_length number of bids in each bidder's running average.
        """

        if len(bid_responses) == 0:
            return

        for bid in bid_responses:
            if bid['id'] in self.averages:
                n = self.window_length
                oldAvg = self.averages[bid['id']]
                newBid = bid['bid_price']
                # Below weighs early bids too much initially
                newAvg = (oldAvg * (n - 1.0) / n) + (newBid / n)
                self.averages[bid['id']] = newAvg
            else:
                self.averages[bid['id']] = bid['bid_price']


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
