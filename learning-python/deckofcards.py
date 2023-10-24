import random
from itertools import combinations

class MyCards:
  """A class to represent a deck of cards."""

  VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
  SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']

  def __init__(self):
    """Initializes a new deck of cards."""
    self.deck = []
    self.build()

  def build(self):
    """Builds the deck of cards."""
    self.deck = [(value, suit) for value in self.VALUES for suit in self.SUITS]

  def join(self, iterable, sep=' '):
    """Joins the elements of an iterable into a string, separated by a separator."""
    return sep.join(map(str, iterable))

  def card_combinations(self, num):
    """Generates all possible combinations of `num` cards from the deck."""
    return {self.join(combos) for combos in combinations(self.deck, num)}

  def pick_random_cards(self, count):
    """Picks a random sample of `count` cards from the deck."""
    return random.sample(self.deck, abs(count))

  def shuffle_cards(self, repeat=1):
    """Shuffles the deck of cards `repeat` times."""
    for _ in range(abs(repeat)):
      random.shuffle(self.deck)

  def print_cards(self):
    """Prints the deck of cards."""
    print(self.deck)

# Create a new deck of cards.
cards = MyCards()

# Shuffle the deck of cards.
cards.shuffle_cards()

# Print all combinations for 2 pair of cards.
print(cards.card_combinations(4))

# Pick 4 random cards.
print(cards.pick_random_cards(4))

# Print all cards.
cards.print_cards()

