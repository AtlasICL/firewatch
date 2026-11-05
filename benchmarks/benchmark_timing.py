import time

import numpy as np


def benchmark(func, input_data, num_runs=100):
    run_times = []
    for i in range(num_runs):
        start = time.perf_counter()
        func(input_data)
        run_times.append(time.perf_counter() - start)
    return np.mean(run_times)
