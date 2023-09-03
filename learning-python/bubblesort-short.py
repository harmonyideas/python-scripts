import random


def bubblesort_short(a_list):
    swap = True
    numpasses = len(a_list) - 1
    while numpasses > 0 and swap:
        swap = False
        for i in range(numpasses):
            if a_list[i] > a_list[i + 1]:
                swap = True
                a_list[i], a_list[i+1] = a_list[i+1], a_list[i]
        numpasses = numpasses - 1
    return a_list


a_list = random.sample(range(100), 100)
print bubblesort_short(a_list)
