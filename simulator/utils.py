# Created by Brian Levis on 3/17/18
import gzip
import json

import sys

import boto3
import os
from botocore.exceptions import ClientError

MIN_PYTHON = (3, 3)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# Approximate number of files in each directory
FILES_PER_HOUR = 32

FILE_FORMAT = '%02d/%02d/part-00%03d.gz'

CB_BUCKET_NAME = 'codebase-pm-dpf'
cb_bucket = boto3.resource('s3').Bucket(name=CB_BUCKET_NAME)

# Features: {'f_nfto', 'token', 'geo_dma_code', 'vi_cnt', 'geo_timezone', 'ua_name', 'c_cnt', 'geo_region_name',
# 'bid_requests', 'geo_country_code2', 'ad_type', 'advertiser_id', 'ad_network_id', 'ua_device', 'txn_rate',
# 'i_txn_fee', 'cr_cnt', 'c_txn_fee', 'r_num_ads_third_party', 'creative_id', 'bid_responses', 'r_cnt', 'vv_cnt',
# 'pub_network_id', 'f_timestamp', 'geo_continent_code', 'i_timestamp', 'zone_id', 'r_num_ads_requested', 'i_cnt',
# 'session_id', 'i_txn_rate', 'rate_metric', 'geo_city_name', 'f_cnt', 'vi_timestamp', 'f_nff', 'c_timestamp',
# 'c_txn_rate', 'campaign_type', 'exp_mode', 'f_nfr', 'campaign_id', 'txn_fee', 'site_id', 'geo_area_code',
# 'vv_timestamp_v', 'r_num_ads_returned', 'r_timestamp', 'ua_os', 'ua_device_type', 'ua_os_name'}
# Removed: {'r_num_ads_returned', 'bid_responses', 'advertiser_id', 'campaign_id', 'f_nfr', 'txn_fee', 'f_cnt', 'f_nff',
#           'vv_cnt', 'i_txn_rate', 'vv_timestamp_v', 'c_txn_rate', 'i_txn_fee', 'cr_cnt', 'c_txn_fee', 'f_nfto',
#           'token', 'vi_cnt', 'txn_rate', 'c_cnt',  'i_cnt', 'vi_timestamp', 'c_timestamp', 'i_timestamp',
#           'f_timestamp', 'session_id', 'ad_network_id',}

BID_RESPONSE_KEY = 'bid_responses'
BID_PRICE_KEY = 'bid_price'
INPUT_FEATURES = {
    'geo_dma_code', 'geo_timezone', 'ua_name', 'geo_region_name', 'bid_requests', 'geo_country_code2', 'ad_type',
    'ua_device', 'r_num_ads_third_party', 'creative_id', 'r_cnt', 'pub_network_id', 'geo_continent_code', 'zone_id',
    'r_num_ads_requested', 'rate_metric', 'geo_city_name', 'campaign_type', 'exp_mode', 'site_id', 'geo_area_code',
    'r_timestamp', 'ua_os', 'ua_device_type', 'ua_os_name'
}


def prepare_line(line, input_features=INPUT_FEATURES):
    # line_dict = json.loads(line)
    processed_line = {
        'bids': [br[BID_PRICE_KEY] for br in line[BID_RESPONSE_KEY]],
        'bid_responses': line[BID_RESPONSE_KEY],
        'input_features': {f: line[f] for f in input_features if f in line}
    }
    processed_line['bids'].sort()
    processed_line['bids'].reverse()
    return processed_line


def calculate_revenue(bids, price_floor):
    # If there are no bids above the price floor
    if len(bids) == 0 or bids[0] < price_floor:
        return 0
    # If there is one bid above the price floor
    if len(bids) == 1 or bids[1] < price_floor:
        return price_floor
    # If there are two bids above the price floor
    return bids[1]


def get_line_iterator(start=(11, 0), stop=(11, 0), limit=None, dictionary=True, download=True, delete=True):
    """
    :param start: (day, hour), inclusive
    :param stop: (day, hour), inclusive
    :param limit: maximum number of files to download
    :param dictionary: yield lines in dict-format
    :param download: download data files before simulation
    :param delete: download data files before simulation
    """
    assert len(start) == len(stop) == 2
    day_start, day_stop = start[0], stop[0]
    hour_start, hour_stop = start[1], stop[1]
    assert day_start in range(11, 16) and day_stop in range(11, 16)
    assert hour_start in range(0, 24) and hour_start in range(0, 24)
    assert day_start * 24 + hour_start <= day_stop * 24 + hour_stop

    file_keys = []
    for d in range(day_start, day_stop + 1):
        for h in range(hour_start if d == day_start else 0, hour_stop + 1 if d == day_stop else 24):
            for n in range(0, FILES_PER_HOUR):
                if limit is not None and len(file_keys) >= limit:
                    break
                file_keys.append(FILE_FORMAT % (d, h, n))
            if d >= day_stop and h >= hour_stop:
                break

    for file_key in file_keys:
        file_name = file_key.replace('/', '_')
        if download:
            try:
                cb_bucket.download_file(Key=file_key, Filename=file_name)
            except ClientError:
                print('Warning: Could not download', file_key)
                continue
        try:
            with gzip.open(file_name, 'rt') as f:
                lines = f.readlines()
                f.close()
        except IOError:
            # TODO: add warning message, replace IOError with correct error
            print("if you can see this, fix the code yourself :D just replace IOError with the one you got")
            continue
        print(file_name)
        for line in lines:
            yield json.loads(line) if dictionary else line
        if delete:
            try:
                os.remove(file_name)
            except OSError:
                print("Warning: Could not delete", file_name)
