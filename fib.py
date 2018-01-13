def fib(n):
    if n < 2:
        return n
    else:
        return F(n - 1) + F(n - 2)

for i in range(0,35):
    print "[" + str(i)  + ":" + str(F(i)) + "]",
