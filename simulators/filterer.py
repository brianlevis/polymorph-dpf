import gzip
import json

import boto3
import os

s3 = boto3.resource('s3')
s3client = boto3.client('s3')

as_bucket_name = 'adsnative-sigmoid'
cb_bucket_name = 'codebase-pm-dpf'

TEMP_INPUT_FILE_NAME = 'temp_in.gz'
TEMP_OUTPUT_FILE_NAME = 'temp_out.gz'


START_INDEX = 0   # [0, 987]
STOP_INDEX = 100  # [1, 988]

try:
    os.remove(TEMP_INPUT_FILE_NAME)
except OSError:
    pass
try:
    os.remove(TEMP_OUTPUT_FILE_NAME)
except OSError:
    pass

as_objects = s3client.list_objects_v2(Bucket=as_bucket_name)

as_bucket = s3.Bucket(name=as_bucket_name)
cb_bucket = s3.Bucket(name=cb_bucket_name)

file_keys = [item['Key'] for item in as_objects['Contents'] if 'part' in item['Key']][START_INDEX:STOP_INDEX]

keys_to_pop = [
    # Duplicate Keys
    "r_timestamp", "pub_network_id", "geo_country_code2", "site_id", "session_id", "geo_continent_code", "zone_id",
    # Unique Keys
    "bid_req_cnt", "bid_resp_cnt", "bid_price", "campaign_id"
]

limiter = 0
limit = 100
for file_key in file_keys:
    if limiter == limit:
        break
    limiter += 1

    print(file_key)

    as_bucket.download_file(Key=file_key, Filename=TEMP_INPUT_FILE_NAME)

    with gzip.open(TEMP_INPUT_FILE_NAME, 'rt') as f:
        lines = f.readlines()
        f.close()
    filtered_output = gzip.open(TEMP_OUTPUT_FILE_NAME, 'wt')

    index = 0
    while index < len(lines):
        line_dict = json.loads(lines[index])
        index += 1
        if "bid_requests" in line_dict and len(line_dict["bid_requests"]) > 0:
            bid_line_dict = json.loads(lines[index])
            for k in keys_to_pop:
                bid_line_dict.pop(k, None)
            line_dict.update(bid_line_dict)
            index += len(line_dict["bid_requests"])
            line = json.dumps(line_dict)
            filtered_output.write(line + "\n")
    filtered_output.close()

    cb_bucket.upload_file(Filename=TEMP_OUTPUT_FILE_NAME, Key=file_key)
