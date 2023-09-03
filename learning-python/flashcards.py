import random


class FlashCards(object):
    def __init__(self):
        self.value = range(0, 10)

    def pick_random_cards(self, operation, x, y):
        result = {
            'M': lambda x, y: x * y,
            'D': lambda x, y: x / y,
            'A': lambda x, y: x + y,
            'S': lambda x, y: x - y,
        }
        return result[operation](x, y)

    def show_flashcard(self, operand):
        operand_symbols = {
            'M': "*",
            'D': "/",
            'A': "+",
            'S': "-",
        }[operand]

        while True:
            x = random.choice(self.value)
            y = random.choice(self.value)
            problem = "%d %s %d = " % (x, operand_symbols, y)
            answer = self.pick_random_cards(operand, x, y)
            user_answer = input(problem)

            if user_answer == str(answer):
                print("You are correct!\n")
            elif user_answer == "Q":
                break


myCards = FlashCards()
myCards.show_flashcard('A')
