import json
from dpf import DynamicPriceFloor


f = open('data')

i = 0

dpf = DynamicPriceFloor()

revenues = []

for line in f:
    line = json.loads(line)
    if 'bid_responses' not in line:
        continue 
    bid_responses = line['bid_responses']
    if len(bid_responses) < 2:
        continue
    bids = []
    for bid in bid_responses:
        bids.append(bid['bid_price'])
    pf = dpf.get_price_floor(len(bids))
    revenue = dpf.update(bids, pf)
    revenues.append(revenue)


print('total revenue:', sum(revenues), ' average revenue:', sum(revenues)/len(revenues))
