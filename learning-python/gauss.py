#!/usr/bin/python
# Gauss forumula for finding the sum of a sequence of numbers


def sum_numbers(num_seq):
    s = len(num_seq) * (num_seq[0] + num_seq[-1]) // 2
    return s


my_num_seq = list(range(1, 101))
print(sum_numbers(my_num_seq))
