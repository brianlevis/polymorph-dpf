import utilities.tools as tools


class Simulator:
    def __init__(self, strategy):
        self.steps = 0
        self.revenues = []
        self.reserve_prices = []
        self.strategy = strategy

    @classmethod
    def auto_file_run(cls, test, data_filename):
        simulator = cls(test)
        with open(data_filename) as file:
            data_stream = tools.get_clean_data(file)
            simulator.run_auction(data_stream)
        return simulator.revenues

    def run_auction(self, data_stream):
        for auction_data in data_stream:
            bid_prices = tools.get_bid_prices(auction_data)
            reserve_price = self.strategy.get_reserve()
            self.run_auction_step(bid_prices, reserve_price)
            self.strategy.update(auction_data, bid_prices, reserve_price)

    def run_auction_step(self, bid_prices, reserve_price):
        sales_price = self._get_sales_price(bid_prices, reserve_price)
        self.steps += 1
        self.reserve_prices.append(reserve_price)
        self.revenues.append(sales_price)

    @staticmethod
    def _get_sales_price(bid_prices, reserve_price):
        if not bid_prices or reserve_price > bid_prices[0]:
            return 0
        if len(bid_prices) == 1:
            return bid_prices[0]
        return max(bid_prices[1], reserve_price)


class Strategy:
    def get_reserve(self):
        raise NotImplementedError()

    def update(self, auction_info, bid_prices, previous):
        raise NotImplementedError()
