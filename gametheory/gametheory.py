import simulator.simulator as sim

DEFAULT_FLOOR = 0.1 / 1000

class GameTheory(sim.Simulator):
    """
    Currently uses an *approximate* running average that doesn't require
    tracking past elements.
    """

    def __init__(self, window, weight, start=(11, 0), stop=(15, 23), 
                 limit=None, download=True, delete=True): 
        Simulator.__init__(self, start, stop, limit, download, delete)
        self.window = window
        self.weight = weight
        self.lowAvg = 0.0
        self.highAvg = 0.0

    def calculate_price_floor(self, input_features):
        return self.lowAvg * self.weight + self.highAvg * (1 - self.weight)

    def process_line(self, line, input_features, bids):
        if len(bids) < 2:
            return
        self.lowAvg = self.lowAvg * (self.window - 1)/self.window +\
                bids[1] * 1.0/self.window
        self.highAvg = self.highAvg * (self.window - 1)/self.window +\
                bids[1] * 1.0/self.window

class GameTheory(sim.Simulator):
    """
    Currently uses an *approximate* running average that doesn't require
    tracking past elements.
    """

    def __init__(self, window, weight, attribute, start=(11, 0), stop=(15, 23), 
                 limit=None, download=True, delete=True): 
        Simulator.__init__(self, start, stop, limit, download, delete)
        self.window = window
        self.weight = weight
        self.attr = attribute
        self.averages = {}
        self.counts = {}

    def calculate_price_floor(self, input_features):
        key = input_features[self.attr]
        if key in self.averages:
            return self.averages[key]
        else: 
            return DEFAULT_FLOOR

    def process_line(self, line, input_features, bids):
        key = input_features[self.attr]
        low, high = bids[1], bids[0]
        weightedAvg = low * self.weight + high * (1 - self.weight)
        if key in self.averages:
            self.averages[key] = self.averages[key] * (self.window - 1)/self.window +\
                    weightedAvg * 1.0/self.window
            self.counts[key] += 1
        else:
            self.averages[key] = weightedAvg
            self.counts[key] = 1