import timeit

def fib(n, index = {0: 0, 1: 1}):
    if n < 2:
        return n

    if n not in index:
        index[n] = fib(n - 1, index) + fib(n - 2, index)
    return index[n]

timer = timeit.Timer(stmt='fib(1)', setup="from __main__ import fib")
print(timer.timeit(number=1))
