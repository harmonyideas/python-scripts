import random
import itertools


class MyCards(object):
    def __init__(self, counter=0):
        self.value = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
        self.rank = ['c', 'd', 'h', 's']
        self.deck = range(52)
        self.deck = [(A + B) for A in self.value for B in self.rank]

    def join(self, iterable, sep=' '):
        """Join the items in iterable, mapping each to a string first."""
        return sep.join(map(str, iterable))

    def card_combinations(self, cards, n):
        return {self.join(combos)
                for combos in itertools.combinations(cards, n)}

    def pick_random_cards(self, counter):
        return random.sample(self.deck, abs(counter))

    def shuffle_cards(self, repeat=1):
        for x in range(0, abs(repeat)):
            random.shuffle(self.deck)

    def print_cards(self):
        # for x in range(len(FlashCards.deck)):
        print self.deck


cards = MyCards()
cards.shuffle_cards(100)

# Give me all combinations for 2 pair of cards
print (cards.card_combinations(cards.deck, 2))

# Give me 4 random cards
print (cards.pick_random_cards(4))
