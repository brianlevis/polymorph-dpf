import json
from dpf import DynamicPriceFloor


f = open('part-#####')

i = 0

hs = [0.1 * i for i in range(1, 10)]
es = [0.1 * i for i in range(1, 10)]
ls = [0.1 * i for i in range(1, 10)]
Ms = [i for i in range(1, 10)]

max_df = None
max_revenue = -1

for h in hs:
    print(h)
    for e in es:
        for l in ls:
            for M in Ms:
                dpf = DynamicPriceFloor(lamb_h=h, lamb_e=e, lamb_l=l, M=M)
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

                total_revenue = sum(revenues)
                if total_revenue > max_revenue:
                    max_dpf = dpf
                    max_revenue = total_revenue


      
print(max_revenue)              
print(max_dpf)

print('total revenue:', sum(revenues), ' average revenue:', sum(revenues)/len(revenues))
