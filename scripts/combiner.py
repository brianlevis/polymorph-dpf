import boto3
import os

import botocore

s3 = boto3.resource('s3')
s3client = boto3.client('s3')

cb_bucket_name = 'codebase-pm-dpf'

TEMP_INPUT_FILE_NAME_1 = 'temp_in0.gz'
TEMP_INPUT_FILE_NAME_2 = 'temp_in1.gz'
TEMP_OUTPUT_FILE_NAME = 'temp_out.gz'

# Total Files: 15,360
START_INDEX = 0
STOP_INDEX = 15360

try:
    os.remove(TEMP_INPUT_FILE_NAME_1)
except OSError:
    pass
try:
    os.remove(TEMP_INPUT_FILE_NAME_2)
except OSError:
    pass
try:
    os.remove(TEMP_OUTPUT_FILE_NAME)
except OSError:
    pass

cb_bucket = s3.Bucket(name=cb_bucket_name)

file_keys = []
for d in range(11, 16):
    for h in range(0, 24):
        for n in range(0, 64):
            input1 = '%02d/%02d/part-00%03d.gz' % (d, h, 2 * n)
            input2 = '%02d/%02d/part-00%03d.gz' % (d, h, 2 * n + 1)
            output = '%02d_reduced/%02d/part-00%03d.gz' % (d, h, n)
            file_keys.append((input1, input2, output))

file_keys = file_keys[START_INDEX:STOP_INDEX]

for input1, input2, output in file_keys:
    print(input1, input2, '>', output)
    failed = [False, False]
    try:
        cb_bucket.download_file(Key=input1, Filename=TEMP_INPUT_FILE_NAME_1)
    except botocore.exceptions.ClientError:
        print("Warning: could not download", input1)
        failed[0] = True
    try:
        cb_bucket.download_file(Key=input2, Filename=TEMP_INPUT_FILE_NAME_2)
    except botocore.exceptions.ClientError:
        print("Warning: could not download", input2)
        failed[1] = True
    if failed[0] and failed[0]:
        print("Warning: could not upload", output)
        break
    elif failed[0]:
        os.system('mv %s %s' % (TEMP_INPUT_FILE_NAME_1, TEMP_OUTPUT_FILE_NAME))
    elif failed[1]:
        os.system('mv %s %s' % (TEMP_INPUT_FILE_NAME_2, TEMP_OUTPUT_FILE_NAME))
    else:
        os.system('cat %s %s > %s' % (TEMP_INPUT_FILE_NAME_1, TEMP_INPUT_FILE_NAME_2, TEMP_OUTPUT_FILE_NAME))
    cb_bucket.upload_file(Filename=TEMP_OUTPUT_FILE_NAME, Key=output)
