import timeit
import functools


def timef(func):
    """https://realpython.com/lessons/timing-functions-decorators/
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kargs):

        start_time = timeit.default_timer()
        value = func(*args, **kargs)
        end_time = timeit.default_timer()
        run_time = end_time - start_time

        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer
