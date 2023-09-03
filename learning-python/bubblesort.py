import random


def bubble_sort(a_list):
    for passnum in range(len(a_list)-1, 0, -1):
        for i in range(passnum):
            if  a_list[i] > a_list[i + 1]:
                a_list[i], a_list[i+1] = a_list[i+1], a_list[i]
    return a_list

a_list = random.sample(range(100), 100)

bubble_sort(a_list)
