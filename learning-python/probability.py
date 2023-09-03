from math import factorial
import random
import itertools


def choices(x, y):
    return factorial(x) // (factorial(x - y) * factorial(y))


def combine(a, b):
    """Concatenate/Merge two dictionaries"""
    return {A + B
            for A in a for B in b}


def join(iterable, sep=' '):
    """Join the items in iterable, mapping each to a string first."""
    return sep.join(map(str, iterable))


def combo(items, n):
    """ Input elements are unique and will be treated as such - not based on position """  
    return {join(combos)
      for combos in itertools.combinations(items, n)}


def find(items, search, n):
    return {s for s in items if s.count(search) == n}


#cards = combine('A23456789TJQK', 'CHDS')
#cards_combos = combo(cards, 2)

