import time


def benchmark(func, input_data):
    start = time.perf_counter()
    func(input_data)
    time_elapsed = time.perf_counter() - start
    print("Execution time:", time_elapsed)
    return time_elapsed
