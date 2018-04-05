from simulator import *


class OneShot:

    def __init__(self, price_floor=0.0002, eps=1.0, lamb_h=0.1, lamb_e=0.46, lamb_l=0.1, time=0, M=5):
        self.price_floor = price_floor
        self.eps = eps
        self.lamb_h = lamb_h
        self.lamb_e = lamb_e
        self.lamb_l = lamb_l
        self.time = time
        self.M = M
        self.revenues = []
        self.oneshot_min_n = 2

    def oneshot(self, first, second):
        if self.price_floor > first:
            self.price_floor = (1 - (self.eps**self.time)*self.lamb_h)*self.price_floor
        elif self.price_floor > second:
            self.price_floor = (1 + (self.eps**self.time)*self.lamb_e)*self.price_floor
        else:
            self.price_floor = (1 + (self.eps**self.time)*self.lamb_l)*self.price_floor
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

    def calculate_differential(self, first, second, price_floor):
        if price_floor > first or price_floor < second:
            return 0.0
        return price_floor - second

    def calculate_price_floor(self, num_bids):
        return self.price_floor

    def update(self, bids, price_floor):
        first, second = self.max2(bids)
        revenue = self.calculate_revenue(first, second, price_floor)
        diff = self.calculate_differential(first, second, price_floor)
        # print(first, second, price_floor, revenue, diff, self.revenues)
        if len(bids) >= self.oneshot_min_n:
            self.oneshot(first, second)
        else:
            if len(self.revenues) == 5:
                self.revenues.pop(0)
            self.revenues.append(revenue)
        return revenue

    def __str__(self):
        return "price_floor: " + str(self.price_floor) + "\neps: " + str(self.eps) + "\nlamb_h: " + str(self.lamb_h) + "\nlamb_e: " + str(self.lamb_e) + "\nlamb_l: " + str(self.lamb_l) + "\ntime: " + str(self.time) + "\nM: " + str(self.M)


class OneShotSimulator(Simulator):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.d = dict()

    def calculate_price_floor(self, input_features):
        if not input_features.get('ad_network_id', 0):
            input_features['ad_network_id'] = 'None'
        
        if not self.d.get(input_features['ad_network_id'] ,0):
            self.d[input_features['ad_network_id']] = OneShot()            

        return self.d[input_features['ad_network_id']].calculate_price_floor(2)

    def process_line(self, line, input_features, bids):
        if not input_features.get('ad_network_id', 0):
            input_features['ad_network_id'] = 'None'
        
        if not self.d.get(input_features['ad_network_id'] ,0):
            self.d[input_features['ad_network_id']] = OneShot()
            
        pf = self.d[input_features['ad_network_id']].price_floor
        self.d[input_features['ad_network_id']].update(bids, pf)
            

if __name__ == "main":
    oneshot = OneShotSimulator(stop=(11, 0), limit=10, delete=False)
    oneshot.run_simulation()
