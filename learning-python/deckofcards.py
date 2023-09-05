import random, itertools

class MyCards():

    VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']

    def __init__(self):
        self.deck = []
        self.build()

    def build(self):
        self.deck = [(value, suit) for value in self.VALUES for suit in self.SUITS]

    def join(self, iterable, sep=' '):
        return sep.join(map(str, iterable))

    def card_combinations(self, num):
        return {self.join(combos) for combos in itertools.combinations(self.deck, num)}

    def pick_random_cards(self, count):
        return random.sample(self.deck, abs(count))

    def shuffle_cards(self, repeat=1):
        for _ in range(abs(repeat)):
            random.shuffle(self.deck)

    def print_cards(self):
        print(self.deck)

cards = MyCards()
cards.shuffle_cards(1)

# Print all combinations for 2 pair of cards
#print(cards.card_combinations(2))

# 4 random cards
# print(cards.pick_random_cards(4))
