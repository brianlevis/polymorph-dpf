import gzip
import json
import boto3
import os

s3 = boto3.resource('s3')
s3client = boto3.client('s3')

input_bucket = 'adsnative-sigmoid'
output_bucket = 'codebase-pm-vw-team'

TEMP_INPUT_FILE_NAME = 'temp_in.gz'

file_keys = []
for d in range(11, 18):
    for n in range(0, 128):
        file_keys.append('%02d/16/part-00%03d.gz' % (d, n))

as_bucket = s3.Bucket(name=input_bucket)
cb_bucket = s3.Bucket(name=output_bucket)

for file_key in file_keys:

    as_bucket.download_file(Key=file_key, Filename=TEMP_INPUT_FILE_NAME)

    with gzip.open(TEMP_INPUT_FILE_NAME, 'r') as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]

    soldbids = []

    for d in lines:
        line_dict = json.loads(d)
        if "bid_resp_cnt" in line_dict:
            if int(line_dict["bid_resp_cnt"]) > 0:
                soldbids.append(line_dict)

    text_file_name = file_key[:2] + file_key[6:-2] + 'txt'
    text_file = open(text_file_name, 'w+')

    #with open(file_key[:-2] + 'txt', "w") as text_file:
    for i in soldbids:
        #print("{0} | siteId:{1} campaignId:{2} zoneId:{3}".format(i["bid_price"], i["site_id"], i["campaign_id"], i["zone_id"]), file=text_file)
        text_file.write("{0} | siteId:{1} campaignId:{2} zoneId:{3}\n".format(i["bid_price"], i["site_id"], i["campaign_id"], i["zone_id"]))
    text_file.close()

    cb_bucket.upload_file(Filename=text_file_name, Key=text_file_name)

    os.remove(TEMP_INPUT_FILE_NAME)
    os.remove(text_file_name)
