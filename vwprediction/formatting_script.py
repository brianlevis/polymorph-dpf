import boto3

import sys
import os
sys.path.append(os.path.abspath('../simulator'))
import utils

START = (12, 0)
END = (12, 2)

utils.INPUT_FEATURES.add('campaign_id')

FILE_NAME = '{0}{1}to{2}{3}.txt'.format(str(START[0]), str(START[1]), str(END[0]), str(END[1]))

line_iterator = utils.get_line_iterator(START, END)

text_file = open(FILE_NAME, 'w+')

def get_features(processed_line):
    campaign_id, site_id, zone_id = 0, 0, 0
    if 'site_id' in processed_line['input_features']:
        site_id = processed_line['input_features']['site_id']
    if 'zone_id' in processed_line['input_features']:
        zone_id = processed_line['input_features']['zone_id']
    if processed_line['bids']:
        for br in processed_line['bid_responses']:
            if br['bid_price'] == processed_line['bids'][0]:
                campaign_id = br['id']
    else:
        campaign_id = processed_line['input_features']['campaign_id']
    return (campaign_id, site_id, zone_id)

while True:
    try:
        line_dict = next(line_iterator)
        processed_line = utils.prepare_line(line_dict)
        features = get_features(processed_line)
        if processed_line['bids']:
            text_file.write("{0} | campaign_id:{1} site_id:{2} zone_id:{3}\n".format(processed_line['bids'][0], features[0], features[1], features[2]))
    except StopIteration:
        break

text_file.close()

output_bucket = boto3.resource('s3').Bucket('codebase-pm-vw-team')

output_bucket.upload_file(Filename=FILE_NAME, Key=FILE_NAME)

os.system('vw {0} --holdout_off -f {1}.model'.format(FILE_NAME, FILE_NAME[:-4]))

#os.remove(FILE_NAME)
