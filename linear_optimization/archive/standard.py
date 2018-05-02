class StandardSimulator:
    def __init__(self, strategy):
        self.strategy = strategy

    def calculate_price_floor(self, input_features):
        return self.strategy.get_reserve()

    def process_line(self, line, input_features, bids):
        return self.strategy.update()
