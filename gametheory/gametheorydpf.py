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

from collections import deque

class GameTheoryDPF:
    # generateR, getRevenue

    def __init__(self, bidResponses, auctionsWindow):
        # bid_responses: list of auctions from 'bid_responses' column
        # auctionsWindow: # of previous 2+ bidder auctions used to calulate reserve
        
        self.bids = [a for a in bidResponses if len(a) != 0]
        self.bids2 = self.getTopTwo(self.bids)
        self.window = auctionsWindow

    def getTopTwo(self, bids):
        # Creates copy of bid_responses with only top two bids per auction
        bids2 = []
        for a in bids:
            if len(a) >= 2:
                sortedBids = sorted(a, key=lambda a: a['bid_price'])
                bids2.append([sortedBids[-2]['bid_price'], sortedBids[-1]['bid_price']])

        return bids2

    def calculateReserve(self, window):
        # Calculates average price of the most recent auctions in a window
        return sum(map(lambda x : sum(x) / 2.0, window)) / len(window) 

    def calculateRevenue(self):
        # Calculates the original revenue with no price floor
        return [min(a) for a in self.bids2]

    def simulate(self):
        # Calculates revenue with running avg price floor
        window = deque()
        revenue = []
        reserve = 0.0
        for a in self.bids2:
            prices = a # sorry
            # Price floor not in active until window has enough auctions for
            # running average.
            if len(window) < self.window:
                window.append(prices)
                revenue.append(min(prices))
            else:
                reserve = self.calculateReserve(window)
                # Add most recent auction and remove oldest auction
                window.append(prices)
                window.popleft()
                # Undershot (neutral)
                if reserve < min(prices):
                    revenue.append(min(prices))
                # Overshot (bad)
                elif reserve > max(prices):
                    revenue.append(0.0)
                # In between (good)
                else:
                    revenue.append(reserve)

        return revenue

    def getStats(self):
        # Returns useful stats. Only includes 2+ bidder auctions, since price
        # floor doesn't affect auctions with 0 or 1 bidders.

        origRev = self.calculateRevenue()
        floorRev = self.simulate()
        floorUnder, floorOver, floorBtwn = 0, 0, 0
        # print(origRev[0:10])
        # print(floorRev[0:10])
        # print(len(origRev), len(floorRev), len(self.bids2))
        for (a, b) in zip(origRev, floorRev):
            # Undershot (neutral)
            if a == b:
                floorUnder += 1
            # Overshot (bad)
            elif b == 0:
                floorOver += 1
            # In between (good)
            else:
                floorBtwn += 1

        stats = {}
        stats['numAuctions'] = len(self.bids2)
        stats['windowSize'] = self.window
        # stats['origWinPrices'] = origRev
        # stats['floorWinPrices'] = floorRev
        stats['origRevenue'] = sum(origRev)
        stats['floorRevenue'] = sum(floorRev)
        stats['floorProfit'] = sum(floorRev) - sum(origRev)
        stats['floorUnder'] = floorUnder / len(floorRev)
        stats['floorOver'] = floorOver / len(floorRev)
        stats['floorBtwn'] = floorBtwn / len(floorRev)
        # stats['floorSuccess'] = floorBtwn / len(floorRev)
        
        return stats