import json
import importlib
from scipy import stats

RESPONSES_ATTR = 'bid_responses'
PRICE_ATTR = 'bid_price'


def get_files_stream(file_names):
    """
    :param file_names: [str] list of file names, each corresponding to a data
        file with lines corresponding to distinct JSON objects
    :return: (gen) a generator yielding JSON objects from each file
    """
    for filename in file_names:
        with open(filename) as data_file:
            for line in data_file:
                information = json.loads(line)
                yield information


def get_file_stream(filename):
    """
    :param filename: (str) filename of data file with lines corresponding to
        distinct JSON objects
    :return: (gen) a generator yielding JSON objects from this file
    """
    yield from get_files_stream([filename])


def get_bid_prices(information):
    """
    :param information: (JSON) the JSON object representing the information
        corresponding to one auction, as described in the Polymorph
        specification
    :return: [float] amount for bids placed in decreasing sorted order

    """
    responses = information[RESPONSES_ATTR]
    prices = [response[PRICE_ATTR] for response in responses]
    prices.sort(reverse=True)
    return prices


def describe(array):
    """
    :param array: [num] array to be displayed
    :return: (None) prints out descriptive statistics
    """
    result = stats.describe(array)
    sample = 'size: {}'.format(result.nobs)
    average = 'mean: {:.3}'.format(result.mean)
    overview = 'range: [{:.3}, {:.3}]'.format(*map(float, result.minmax))
    variance = 'var: {:.3}'.format(result.variance)
    print(sample, average, overview, variance, sep='\n', end='\n\n')


def compare(value, reference):
    """
    :param value: (float) value to be compared
    :param reference: (float) baseline with which to calculate difference
    :return: (None) prints out the percentage difference
    """
    difference = (value - reference) / reference
    percent = float(100 * difference)
    direction = 'lower' if difference < 0 else 'higher'
    print('{:.3}% {}'.format(percent, direction))


def reload(*modules):
    """
    :param modules: (Package...) packages to be reloaded
    :return: (None) reloads each of these modules in the current environment
    """
    for library in modules:
        importlib.reload(library)
