for x in range(0,100):
    if (x % 3 == 0) & (x % 5 ==0):
        print ("FIZZBUZZ %d" % x)
    elif (x % 3 == 0):
        print ("FIZZ %d" %x)
    elif (x % 5 ==0):
        print ("BUZZ %d" %x)


