import boto3
import sys
import os
sys.path.append(os.path.abspath('..'))
import simulator.utils as utils

START = (12, 0)
END = (12, 0)

FILE_NAME = 'test.txt'#'{0}{1}to{2}{3}.txt'.format(str(START[0]), str(START[1]), str(END[0]), str(END[1]))

line_iterator = utils.get_line_iterator(START, END, limit=32)

text_file = open(FILE_NAME, 'w+')

while True:
    try:
        line_dict = next(line_iterator)
        processed_line = utils.prepare_line(line_dict)
        if processed_line['bids']:
            line = str(processed_line['bids'][0]) + ' | '
            for feature in processed_line['input_features']:
                if str(feature) == 'bid_requests':
                    for request_id in processed_line['input_features']['bid_requests']:
                        line += 'campaign_id' + str(request_id) + ' '
                elif str(feature) == 'r_timestamp':
                    line += 'hour' + str(processed_line['input_features'][str(feature)])[11:13] + ' '
                elif 'num_ads' in str(feature) or 'r_cnt' in str(feature):
                    line += feature + ':' + str(processed_line['input_features'][str(feature)]) + ' '
                else:
                    line += feature + str(processed_line['input_features'][str(feature)]) + ' '
            line = line[:-1] + '\n'
            text_file.write(line)
    except StopIteration:
        break

text_file.close()

output_bucket = boto3.resource('s3').Bucket('codebase-pm-vw-team')

output_bucket.upload_file(Filename=FILE_NAME, Key=FILE_NAME)

os.system('vw {0} --holdout_off -f {1}.model'.format(FILE_NAME, FILE_NAME[:-4]))

os.remove(FILE_NAME)
