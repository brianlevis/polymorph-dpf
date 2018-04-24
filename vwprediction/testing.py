from simulate import *

'''Testing using 3-day models on 2 hours of data from 2/14.'''
all_revenues = {}
for p in range(1, 6):
    model_name = 'models/%01d_pass' % p
    all_revenues[p] = optimal_multiplier((14, 0), (14, 0), 0.5, 1.5, 0.1, model_name)
print(all_revenues)
