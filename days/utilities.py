from datetime import datetime
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
        start_time = datetime.now()
        value = func(*args, **kwargs)
        end_time = datetime.now()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time} secs")
        return value
    return wrapper_timer