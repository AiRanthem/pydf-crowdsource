from time import time


def bench(reps, func, *args):
    start = time()
    for i in range(0, reps):
        func(*args)
    end = time()
    print(f"{func.__name__}    run {reps} times in {end - start} seconds, {(end - start) / reps} secs / op")
    return (end - start) / reps
