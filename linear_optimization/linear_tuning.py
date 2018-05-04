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
    results = run_queue(limit=1)
    return results


def test_single_heuristic(slope):
    settings = {
        'memory': 30,
        'up': 1,
        'down': slope,
        'discount': 1.0,
        'default': 0.1 / 1000
    }
    test = LinearHeuristic(**settings)
    test.run_simulation()
    test.stats.print_stats()


if __name__ == '__main__':
    input_slope = float(sys.argv[1])
    print(input_slope)
    test_single_heuristic(input_slope)
