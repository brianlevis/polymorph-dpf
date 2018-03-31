import dpf
from random import randint

class MultiShot:
    # oneshots[0] holds sites w/ returns from init_return to init_return+init_gap
    # oneshots[1] similarly for init_return+init_gap to init_return+2*init_gap
    def __init__(self, num_shots, init_return=0.0, init_gap=.05):
        self.num_shots = num_shots
        self.init_return = init_return
        self.init_gap = init_gap
        self.oneshots = [dpf.DynamicPriceFloor() for _ in range(num_shots)]
        self.ids = {} # id -> index of one shot algo

    def get_price_floor(self, input_features):
        site_id, num_bids = input_features['site_id'], len(input_features['bid_requests'])
        if site_id not in self.ids:
            # can also try using average return instead of random
            oneshot = self.oneshots[randint(0, self.num_shots-1)]
            pf = oneshot.get_price_floor(num_bids)
            idx = (pf+self.init_return)//self.init_gap
            self.ids[site_id] = idx
        else:
            pf = self.oneshots[self.ids[site_id]].get_price_floor(num_bids) 
        self.pf = pf 
        
    def update(self, input_features):
        bids = inpute_features['bid_requests']
        if site_id in self.ids and hasattr(self, pf):
            self.oneshots[self.ids[site_id]].update(bids, self.pf)
