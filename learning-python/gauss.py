#!/usr/bin/python
# Gauss forumula for finding the sum of a sequence of numbers


def sum_numbers(num_seq):
    s = (num_seq[-1] / 2) * (num_seq[0] + num_seq[-1])
    return s


num_seq = [i for i in range(1, 101)]
print sum_numbers(num_seq)
