# This example should be recognized from the book "The C Programming Language" EX. 1-4
# Author: Brian W. Kernighan, Dennis M. Ritchie


def temp_conversion_table():

    celsius = 0
    print "{0:^12} {1:^16}".format("Farenheit", "Celsius")

    for fahr in range(0, 300, 20):
        celsius = 5 * (fahr - 32) / 9
        print "{0:^12}{1:^16}".format(fahr, celsius)


temp_conversion_table()
