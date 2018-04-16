class OneShot:

    def __init__(self, price_floor=0.0002, eps=1.0, lamb_h=0.1, lamb_e=0.46, lamb_l=0.1, time=0, M=5, pf_ceil=.005):
        self.price_floor = price_floor
        self.eps = eps
        self.lamb_h = lamb_h
        self.lamb_e = lamb_e
        self.lamb_l = lamb_l
        self.time = time
        self.M = M
        self.revenues = []
        self.oneshot_min_n = 2
        self.log = [0]*3
        self.over = 0
        self.pf_ceil = pf_ceil

    def oneshot(self, first, second):
        if self.price_floor > first:
            self.log[0] += 1
            self.over += self.price_floor
            self.price_floor = (1 - (self.eps**self.time)*self.lamb_h)*self.price_floor
        elif self.price_floor > second:
            self.log[1] += 1
            self.price_floor = (1 + (self.eps**self.time)*self.lamb_e)*self.price_floor
        else:
            self.log[2] += 1
            self.price_floor = (1 + (self.eps**self.time)*self.lamb_l)*self.price_floor
        self.price_floor = min(self.price_floor, self.pf_ceil)
        self.time += 1

    def max2(self, bids):
        max1 = max2 = 0
        for bid in bids:
            if bid > max1:
                max1, max2 = bid, max1
            elif bid > max2:
                max2 = bid
        return max1, max2

    def calculate_revenue(self, bids, price_floor):
        first, second = self.max2(bids)
        return self.calculate_revenue_helper(first, second, price_floor)

    def calculate_revenue_helper(self, first, second, price_floor):
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
        revenue = self.calculate_revenue_helper(first, second, price_floor)
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


#class OneShotSimulator(Simulator):
#    
#    def __init__(self, *args, id='ad_network_id', **kwargs):
#        super().__init__(*args, **kwargs)
#        self.d = dict()
#        self.id = id
#
#    def calculate_price_floor(self, input_features):
#        if not input_features.get(self.id, 0):
#            input_features[self.id] = 'None'
#        
#        if not self.d.get(input_features[self.id], 0):
#            self.d[input_features[self.id]] = OneShot()
#
#        return self.d[input_features[self.id]].calculate_price_floor(2)
#
#    def process_line(self, line, input_features, bids):
#        if not input_features.get(self.id, 0):
#            input_features[self.id] = 'None'
#        
#        if not self.d.get(input_features[self.id], 0):
#            self.d[input_features[self.id]] = OneShot()
#            
#        pf = self.d[input_features[self.id]].price_floor
#        self.d[input_features[self.id]].update(bids, pf)
#            
#
#if __name__ == "__main__":
#    oneshot = OneShotSimulator(stop=(11, 0), limit=10, delete=False)
#    oneshot.run_simulation()
