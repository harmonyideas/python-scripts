import random

def bubblesort_short(a_list):
    for numpasses in range(len(a_list) - 1, 0, -1):
        swap = False
        for i, value in enumerate(a_list[:-1]):
            if value > a_list[i + 1]:
                a_list[i], a_list[i + 1] = a_list[i + 1], a_list[i]
                swap = True
        if not swap:
            break
    return a_list

my_list = random.sample(range(100), 100)
print(bubblesort_short(my_list))
