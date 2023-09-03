import random


class Cards(object):
    def __init__(self, counter=0):
        self.value = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
        self.rank = ['c', 'd', 'h', 's']
        Cards.deck = range(52)
        Cards.deck = [(A + B) for A in self.value for B in self.rank]

    def pick_random_cards(self, counter):
        return random.sample(Cards.deck, abs(counter))

    def shuffle_cards(self, repeat=1):
        for i in range(0, abs(repeat)):
            random.shuffle(Cards.deck)

    def print_cards(self):
        # for x in range(len(FlashCards.deck)):
        print Cards.deck


myCards = Cards()
myCards.shuffle_cards(1)
print (myCards.pick_random_cards(4))

# print myCards.pick_random_cards(4)
