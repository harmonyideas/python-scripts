import timeit


def fib(n):
    i = 0
    first=0
    last = 1

    while i < n:
        yield last
        first, last = last, first + last
        i += 1

for x in fib(10): 
    print(x)


