import gzip
import json
import boto3

import sys
import os
sys.path.append(os.path.abspath('../simulator'))
import utils

line_iterator = utils.get_line_iterator((11, 0), (11, 0))

text_file = open('formatted.txt', 'w+')

while True:
    try:

        line_dict = next(line_iterator)
        processed_line = utils.prepare_line(line_dict)

        campaign_id, site_id, zone_id = 0, 0, 0

        if 'site_id' in processed_line['input_features']:
            site_id = processed_line['input_features']['site_id']
        if 'zone_id' in processed_line['input_features']:
            zone_id = processed_line['input_features']['zone_id']
        if processed_line['bids']:
            for br in processed_line['bid_responses']:
                if br['bid_price'] == processed_line['bids'][0]:
                    campaign_id = br['id']
            text_file.write("{0} | campaign_id:{1} site_id:{2} zone_id:{3}\n".format(processed_line['bids'][0], campaign_id, site_id, zone_id))
    except StopIteration:
        break

text_file.close()

output_bucket = boto3.resource('s3').Bucket('codebase-pm-vw-team')

output_bucket.upload_file(Filename='formatted.txt', Key='formatted.txt')

os.remove('formatted.txt')
