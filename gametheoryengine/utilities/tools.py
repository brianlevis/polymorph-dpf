import json
import importlib

RESPONSES_ATTR = 'bid_responses'
PRICE_ATTR = 'bid_price'


def get_clean_data(data_file):
    for line in data_file:
        information = json.loads(line)
        yield information


def get_bid_prices(information):
    responses = information[RESPONSES_ATTR]
    prices = [response[PRICE_ATTR] for response in responses]
    prices.sort(reverse=True)
    return prices


def reload(*modules):
    for library in modules:
        importlib.reload(library)
