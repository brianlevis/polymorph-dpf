from collections import deque

from simulator import *


class RunningAverageWithZeros(Simulator):
    """Represents a simple running average floor, where 0 is added to the average if there are no bids."""

    def __init__(self, *args, history_len=250, weight=25.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.most_recent_bids = deque([0] * history_len, maxlen=history_len)
        self.weight = weight

    def calculate_price_floor(self, input_features):
        return self.weight * sum(self.most_recent_bids) / self.most_recent_bids.maxlen

    def process_line(self, line, input_features, bids):
        bid = 0.0 if len(bids) == 0 else bids[0]
        self.most_recent_bids.append(bid)


class RunningAverageWithoutZeros(Simulator):
    """Represents a simple running average floor."""

    def __init__(self, *args, history_len=25, weight=0.45, **kwargs):
        super().__init__(*args, **kwargs)
        self.most_recent_bids = deque([0] * history_len, maxlen=history_len)
        self.weight = weight

    def calculate_price_floor(self, input_features):
        return self.weight * sum(self.most_recent_bids) / self.most_recent_bids.maxlen

    def process_line(self, line, input_features, bids):
        if len(bids) > 0:
            self.most_recent_bids.append(bids[0])


class BucketedRunningAverageWithZeros(Simulator):
    """Represents a simple running average floor."""

    def __init__(self, *args, history_len=25, weight=0.45, feature='site_id', **kwargs):
        super().__init__(*args, **kwargs)
        self.history_len = history_len
        self.feature = feature
        self.weight = weight
        self.history = {}

    def calculate_price_floor(self, input_features):
        if input_features[self.feature] not in self.history:
            self.history[input_features[self.feature]] = deque([0], maxlen=self.history_len)
        hist = self.history[input_features[self.feature]]
        return self.weight * sum(hist) / hist.maxlen

    def process_line(self, line, input_features, bids):
        if len(bids) > 0:
            self.history[input_features[self.feature]].append(bids[0])


class BucketedRunningAverageWithoutZeros(Simulator):
    """Represents a simple running average floor."""

    def __init__(self, *args, history_len=8, weight=1.6, feature='site_id', **kwargs):
        super().__init__(*args, **kwargs)
        self.history_len = history_len
        self.feature = feature
        self.weight = weight
        self.history = {}

    def calculate_price_floor(self, input_features):
        if input_features[self.feature] not in self.history:
            self.history[input_features[self.feature]] = deque([0], maxlen=self.history_len)
        hist = self.history[input_features[self.feature]]
        return self.weight * sum(hist) / hist.maxlen

    def process_line(self, line, input_features, bids):
        bid = 0.0 if len(bids) == 0 else bids[0]
        self.history[input_features[self.feature]].append(bid)
