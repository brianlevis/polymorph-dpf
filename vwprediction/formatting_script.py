import gzip

import boto3
import sys
import os
sys.path.append(os.path.abspath('..'))
import simulator.utils as utils

FILE_FORMAT = '%02d/part-%02d.vw.gz'

output_bucket = boto3.resource('s3').Bucket('codebase-pm-vw-team')

for d in range(11, 16):
    for h in range(0, 24):
        remote_filename = '%02d/part-%02d.vw.gz' % (d, h)
        local_filename = remote_filename.replace('/', '_')
        local_file = gzip.open(local_filename, 'wt')
        for line_dict in utils.get_line_iterator(start=(d, h), stop=(d, h)):
            processed_line = utils.prepare_line(line_dict)
            if processed_line['bids']:
                line = str(processed_line['bids'][0]) + ' | '
                for feature in processed_line['input_features']:
                    if feature == 'bid_requests':
                        for request_id in processed_line['input_features']['bid_requests']:
                            line += 'campaign_id' + str(request_id) + ' '
                    elif feature == 'r_timestamp':
                        line += 'hour' + str(processed_line['input_features'][feature])[11:13] + ' '
                    elif 'num_ads' in feature or 'r_cnt' in feature:
                        line += feature + ':' + str(processed_line['input_features'][feature]) + ' '
                    else:
                        line += feature + str(processed_line['input_features'][feature]) + ' '
                line = line[:-1] + '\n'
                local_file.write(line)
        local_file.close()
        output_bucket.upload_file(Filename=local_filename, Key=remote_filename)
        os.remove(local_filename)

# os.system('vw {0} --holdout_off -f {1}.model'.format(FILE_NAME, FILE_NAME[:-4]))
