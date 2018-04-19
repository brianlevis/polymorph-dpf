#from simulate import *
import boto3
import gzip
import os
import shutil
import sys
from time import time

'''
pass_dict = {}

for num_passes in range(1, 11):
    if num_passes != 1:
        os.system('vw part-00.vw --holdout_off -c --passes {0} -f {1}.model'.format(num_passes, num_passes))
    else:
        os.system('vw part-00.vw --holdout_off --passes {0} -f {1}.model'.format(num_passes, num_passes))
    pass_dict[num_passes] = optimal_multiplier((12, 0), (12, 0), 0.5, 1, 0.1, num_passes)

print(pass_dict)
'''

input_bucket = boto3.resource('s3').Bucket('codebase-pm-vw-team')
start_time = time()
for d in range(11, 14):
    for h in range(0, 24):
        print('Day: %d, Hour: %d' % (d, h))
        file_key = '%02d/part-%02d.vw.gz' % (d, h)
        file_name = file_key.replace('/', '_')
        input_bucket.download_file(file_key, file_name)
        for p in range(1, 6):
            print('Passes:', p)
            print('Time elapsed', time() - start_time)
            sys.stdout.flush()
            try:
                with gzip.open(file_name, 'rb') as f_in:
                    with open(file_name[:-3], 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                    if p != 1:
                        os.system('vw {0} --holdout_off -c --save_resume --passes {1} -f {2}.model'.format(file_name[:-3], p, p))
                    else:
                        os.system('vw {0} --holdout_off --save_resume --passes {1} -f {2}.model'.format(file_name[:-3], p, p))
                    f_in.close()
                    f_out.close()
            except IOError:
                print("if you can see this, fix the code yourself :D just replace IOError with the one you got")
                continue
        os.remove(file_name)
        os.remove(file_name[:-3])
