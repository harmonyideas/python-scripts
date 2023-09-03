#!/usr/bin/python
# Gauss forumula for summing a sequence of numbers

def sum_numbers(num_seq):
    s = num_seq[-1]*(num_seq[0] + num_seq[-1])/2
    return s

num_seq = [i for i in range(1,11)]
print sum_numbers(num_seq)
