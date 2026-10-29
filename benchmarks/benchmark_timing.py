import time

def benchmark(func, input_data):
    start = time.perf_counter()
    func(input_data)
    time_elapsed = time.perf_counter() - start
    return time_elapsed