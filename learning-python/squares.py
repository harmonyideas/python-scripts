import random

def square_list(my_list):
    squared_list = [ i**2 for i in my_list ]
    print squared_list

numbers = list(xrange(0,25))
square_list(numbers)
