def fib(n):
    
    if n < 2:
        return n

    first, last = 1, 0

    for i in (xrange(n)):
        first, last = last, first + last
    return last


print fib(10)
