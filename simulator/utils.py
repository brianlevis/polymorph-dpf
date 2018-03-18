# Created by Brian Levis on 3/17/18
import random
import string

import sys

MIN_PYTHON = (3, 3)
if sys.version_info < MIN_PYTHON:
    sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

# Approximate umber of files in each directory
FILES_PER_HOUR = 128

# List of files to be deleted
filename_index = {}


def download_files(start=(11, 0, 0), stop=(11, 1, 1)):
    """

    :param start: (day, hour, minute)
    :param stop: (day, hour, minute)
    """
    assert len(start) == len(stop) == 3

    file_keys = []
    day_start, day_stop = start[0], stop[0]
    for d in range(day_start, day_stop + 1):
        first_day, last_day = d == start[0], d == stop[0]
        hour_start, hour_stop = start[1] if first_day else 0, stop[1] if last_day else 23
        for h in range(hour_start, hour_stop + 1):
            first_hour, last_hour = first_day and h == start[1], last_day and h == stop[1]
            minute_start, minute_stop = start[2] if first_hour else 0, stop[2] if last_hour else 59
            index_start = minute_start * FILES_PER_HOUR / 60
            for n in range(0, 128):  # File index
                file_keys.append('%02d/%02d/part-00%03d.gz' % (d, h, n))

    file_names = []
    token = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
    filename_index[token] = file_names
    return token


def delete_files(token):
    pass


def get_line_iterator(token):
    pass
