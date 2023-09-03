def multiplication_table():

    colheaders = ['1', '2', '3', '4', '5', '6',
                  '7', '8', '9', '10', '11', '12']

    rows = range(1, 13)
    cols = range(1, 13)

    for c in colheaders:
        print("\t" + "[" + c + "]"),

    for r in rows:
        print("\n" + "[" + str(r) + "]"),
        for c in cols:
            print("\t" + str(r * c)),
        print("\n")
        
multiplication_table()

