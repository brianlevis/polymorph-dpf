from dpf import OneShot
from random import randint
from simulator import Simulator

class MultiShot(Simulator):
    """oneshots[0] holds sites w/ returns from init_return to init_return+init_gap
    oneshots[1] similarly for init_return+init_gap to init_return+2*init_gap, etc
    """
    def __init__(self, num_shots, init_return=0.0, init_gap=.00005, oneshot_args={}):
        super(MultiShot, self).__init__(limit=10, download=False, delete=False)
        self.num_shots = num_shots
        self.init_return = init_return
        self.init_gap = init_gap
        self.oneshots = [OneShot(**oneshot_args) for _ in range(num_shots)]
        self.ids = {} # id -> index of one shot algo

    def calculate_price_floor(self, input_features):
        site_id, num_bids = input_features['site_id'], len(input_features['bid_requests'])
        if site_id not in self.ids:
            # can also try using average return instead of random
            oneshot = self.oneshots[randint(0, self.num_shots-1)]
            pf = oneshot.calculate_price_floor(num_bids)
            idx = self.get_idx(pf) 
            self.ids[site_id] = idx
        else:
            pf = self.oneshots[self.ids[site_id]].calculate_price_floor(num_bids) 
        self.pf = pf
        return pf
    
       
    def get_idx(self, revenue):
        idx = int((revenue-self.init_return)//self.init_gap)
        return min(idx, self.num_shots-1)
 
    def process_line(self, line, input_features, bids):
        site_id = input_features['site_id']
        if site_id in self.ids and hasattr(self, 'pf'):
            oneshot = self.oneshots[self.ids[site_id]]
            revenue = oneshot.calculate_revenue(bids, self.pf)
            idx = self.get_idx(revenue)
            self.ids[site_id] = idx 
            oneshot.update(bids, self.pf)
            
oneshot_args = {'price_floor': 0.0002, 'eps': 1.0, 'lamb_h': 0.1, 'lamb_e': 0.46, 'lamb_l': 0.1, 'time': 0, 'M': 5}
oneshot = MultiShot(1, oneshot_args=oneshot_args)
oneshot.run_simulation()
print([list(oneshot.ids.values()).count(i) for i in range(oneshot.num_shots)])
print([o.log for o in oneshot.oneshots])

