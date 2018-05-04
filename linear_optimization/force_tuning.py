import sys; sys.path.append('../')

import numpy as np
from simulator import queue_simulator, run_queue
from linear_optimization.clever_brute_force import CleverBruteForce


def test_forcing(discount_range):
    for discount in discount_range:
        settings = {
            'memory': 100,
            'discount': discount,
            'default': 0.1 / 1000
        }

        test = CleverBruteForce(**settings)
        description = 'Forcing: (discount={:.2f})'.format(discount)
        queue_simulator(test, description)
    results = run_queue(limit=3)
    return results


if __name__ == '__main__':
    discounts = np.linspace(0, 1, 25)
    test_forcing(discounts)
