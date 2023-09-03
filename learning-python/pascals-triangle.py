def pascals_triangle():

    rows = range(0, 10)
    coef = 1
      
    for r in rows:
        for z in range(0, len(rows) - r):
            print (""),
        for x in range(0, r + 1):
            if (x == 0 or r == 0):
                coef = 1
            else:
                coef = coef * (r - x + 1) / x
            print (coef),
        print ("\n"),

def pascals_triangle_p3():

    rows = range(0, 10)
    coef = 1

    for r in rows:
        for z in range(0, len(rows) - r):
            print ("", end=" ")
        for x in range(0, r + 1):
            if (x == 0 or r == 0):
                coef = 1
            else:
                coef = coef * (r - x + 1) / x
            print (int(coef), end=" ")
        print ("\n", end=" ")

# Python2
#pascals_triangle()

# Python3
#pascals_triange_p3()
