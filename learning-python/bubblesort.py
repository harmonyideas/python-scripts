import random

def bubble_sort(a_list):
    for passnum in range(len(a_list)-1, 0, -1):
        for i in range(passnum):
            j = i + 1
            if a_list[i] > a_list[j]:
                a_list[i], a_list[j] = a_list[j], a_list[i]
    return a_list

my_list = random.sample(range(100), 100)
bubble_sort(my_list)
