import collections
import utilities.engine as engine


class Constant(engine.Strategy):
    def __init__(self, default=0):
        self.default = default

    def get_reserve(self):
        return self.default

    def update(self, auction_info, bid_prices, previous):
        pass


class GameTheory(engine.Strategy):
    def __init__(self, window_length, fraction):
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
