from simulate import *
import os

pass_dict = {}

for num_passes in range(1, 11):
    if num_passes != 1:
        os.system('vw part-00.vw --holdout_off -c --passes {0} -f {1}.model'.format(num_passes, num_passes))
    else:
        os.system('vw part-00.vw --holdout_off --passes {0} -f {1}.model'.format(num_passes, num_passes))
    pass_dict[num_passes] = optimal_multiplier((12, 0), (12, 0), 0.5, 1, 0.1, num_passes)

print(pass_dict)
