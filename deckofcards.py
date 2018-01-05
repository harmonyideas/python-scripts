import random


class Cards(object):
    def __init__(self, counter=0):
        self.value = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
        self.rank = ['c', 'd', 'h', 's']
        Cards.deck = range(52)

        for x in self.value:
            for y in self.rank:
                Cards.deck[counter] = (x + y)
                counter += 1


def pick_random_cards(counter):
    return random.sample(Cards.deck, abs(counter))


def shuffle_cards(self, repeat=1):
    print "Shuffling Deck:", abs(repeat), "x"
    for x in range(0, abs(repeat)):
        random.shuffle(Cards.deck)


def print_cards(self):
    # for x in range(len(FlashCards.deck)):
    print Cards.deck


myCards = Cards()
print (pick_random_cards(15))

# print myCards.pick_random_cards(4)
