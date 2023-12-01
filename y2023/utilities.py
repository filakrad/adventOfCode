from datetime import datetime
from time import perf_counter
import functools


def add_to_dict(dct, key, value):
    if key in dct:
        dct[key] += value
    else:
        dct[key] = value


def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = perf_counter()
        value = func(*args, **kwargs)
        end_time = perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time} secs")
        return value
    return wrapper_timer