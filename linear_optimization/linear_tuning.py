import sys; sys.path.append('../')

import numpy as np
from simulator import queue_simulator, run_queue
from linear_optimization.linear_heuristic import LinearHeuristic


def test_heuristic(slope_range, discount_range):
    for down_slope in slope_range:
        for discount in discount_range:
            settings = {
                'memory': 30,
                'up': 1,
                'down': down_slope,
                'discount': discount,
                'default': 0.1 / 1000
            }

            test = LinearHeuristic(**settings)
            description = 'Linear: (down={:.2f}, discount={:.2f})'.format(
                down_slope, discount)
            queue_simulator(test, description)
    results = run_queue(limit=3)
    return results


if __name__ == '__main__':
    slopes = np.linspace(-3, -1, 20)
    discounts = np.linspace(1, 1, 1)
    test_heuristic(slopes, discounts)
