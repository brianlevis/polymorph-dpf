class DynamicPriceFloor:

    def __init__():
        self.price_floor = 0.000001
        self.eps = 1.0
        self.lamb_h = .3
        self.lamb_e = .01
        self.lamb_l = .02
        self.time = 0
        self.M = 5
        self.revenues = []

    def oneshot(self, first, second):
        if self.price_floor > first:
            self.price_floor = (1 - (self.eps**self.time)*self.lamb_h)*self.price_floor
        elif self.price_floor > second:
            self.price_floor = (1 + (self.eps**self.time)*self.lamb_e)*self.price_floor
        else:
            self.price_floor = (1 + (self.eps**self.time)*self.lamb_t)*self.price_floor
        self.time += 1

    def max2(self, bids):
        max1 = max2 = 0
        for bid in bids:
            if bid > max1:
                max1, max2 = bid, max1
            elif bid > max2:
                max2 = bid
        return max1, max2

    def calculate_revenue(self, first, second, price_floor):
        if price_floor > first:
            return 0.0
        return max(second, price_floor)

    def get_price_floor(self, num_bids):
        return self.price_floor if num_bids > 10 else sum(revenues)/len(revenues)

    def update(self, bids):
        first, second = self.max2(bids)
        if len(bids) > 10:
            self.oneshot(first, second)
        else:
            if len(rewards) == 5:
                revenues.pop(0)
                revenue = calculate_revenue(first, second, price_floor)
                revenues.append(revenue)
