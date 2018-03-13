# Based on: http://www.cs.ubc.ca/~cs532l/gt2/slides/11-6.pdf
# Simple game theory reserve price.
#
# 2 bidders, valuations v_i uniformly distributed on [0, 1]
# Set reserve price/floor price at 0 < R < 1. Probabilities:
#     P(R below)   = R^2,         revenue = min(v_1, v_2)
#     P(R between) = 2(1 - R)(R), revenue = R
#     P(R above)   = (1 - R^2),   revenue = 0
#
# Expected revenue = [1 + 3R^2 - 4R^3]/3
# Maximize (0 = d/dR): 0 = 2R - 4R^2
# OPTIMAL RESERVE PRICE: R = 1/2
# ESTIMATED REVENUE: 5/12 for R = 1/2 versus 1/3 for R = 0 (no price floor)

from collections import dequeue

class GameTheoryDPF:
    # generateR, getRevenue

    def __init__(bidResponses, auctionsWindow):
        # bid_responses: list of auctions from 'bid_responses' column
        # auctionsWindow: # of previous non-zero auctions used to calulate reserve
        
        self.bids = [a for a in bid_responses if len(a) != 0]
        self.bids2 = getTopTwo(self.bids)
        self.window = auctionsWindow
        # self.r = 0.0

    def getTopTwo(bids):
        # Creates copy of bid_responses with only top two bids per auction
        bids2 = []
        for a in bids:
            if len(a) >= 2:
                sortedBids = sorted[a, key=lambda a: a['bid_price']]
                bids2.append([sortedBids[-2], sortedBids[-1]])

        return bids2

    def calculateReserve():
        return 

    def calculateRevenue():
        return 

    def simulate():
        window = dequeue()
        revenue = []
        reserve = 0.0
        for a in self.bids2:
            prices = [bid['bid_price'] for bid in a]
            if len(window) < self.window:
                window.append(prices)
                revenue.append(min(prices))
            else:
                reserve = sum(window) / len(window)
                if reserve > max(prices):
                    revenue.append(0)
                else if reserve < min(prices):
                    revenue.append(min(prices))
                else:
                    revenue.append(reserve)

        return revenue
