def bubblesort_short(a_list):
    swap = True
    numpasses = len(a_list) - 1
    while numpasses > 0 and swap:
        swap = False
        for i in range(numpasses):
            if a_list[i] > a_list[i + 1]:
                swap = True
                temp = a_list[i]
                a_list[i] = a_list[i + 1]
                a_list[i + 1] = temp
        numpasses = numpasses - 1
