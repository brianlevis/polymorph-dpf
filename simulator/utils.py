# Created by Brian Levis on 3/17/18
import gzip
import json
import random
import string

import sys

import boto3
import os
from botocore.exceptions import ClientError

MIN_PYTHON = (3, 3)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# Approximate number of files in each directory
FILES_PER_HOUR = 128

CB_BUCKET_NAME = 'codebase-pm-dpf'
cb_bucket = boto3.resource('s3').Bucket(name=CB_BUCKET_NAME)


class FileReader:

    def __init__(self, start=(11, 0), stop=(11, 0), limit=None):
        """
        :param start: (day, hour), inclusive
        :param stop: (day, hour), inclusive
        :param limit: maximum number of files to download
        """
        self.start = start
        self.stop = stop
        self.limit = limit
        self.file_names = []

    def download_files(self):
        assert len(self.start) == len(self.stop) == 2
        day_start, day_stop = self.start[0], self.stop[0]
        hour_start, hour_stop = self.start[1], self.stop[1]
        assert day_start in range(11, 16) and day_stop in range(11, 16)
        assert hour_start in range(0, 23) and hour_start in range(0, 24)
        assert day_start * 24 + hour_start <= day_stop * 24 + hour_stop

        file_keys = []
        for d in range(day_start, day_stop + 1):
            for h in range(hour_start if d == day_start else 0, hour_stop + 1 if d == day_stop else 24):
                for n in range(0, FILES_PER_HOUR):
                    if self.limit is not None and len(file_keys) >= self.limit:
                        break
                    file_keys.append('%02d/%02d/part-00%03d.gz' % (d, h, n))
                if d >= day_stop and h >= hour_stop:
                    break

        for file_key in file_keys:
            try:
                file_name = file_key.replace('/', '_')
                cb_bucket.download_file(Key=file_key, Filename=file_name)
                self.file_names.append(file_name)
            except ClientError:
                print('Warning: Could not download', file_key)

    def delete_files(self):
        for file_name in self.file_names:
            try:
                os.remove(file_name)
            except OSError:
                print("Warning: Could not delete", file_name)

    def get_line_iterator(self, dictionary=False):
        for file_name in self.file_names:
            with gzip.open(file_name, 'rt') as f:
                lines = f.readlines()
                f.close()
            for line in lines:
                yield json.loads(line) if dictionary else line
