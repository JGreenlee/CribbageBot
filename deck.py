from random import shuffle

from card import Card


class Deck:
    def __init__(self):
        self.cards = []
        for j in range(4):
            for k in range(1, 14):
                self.cards.append(Card(j, k))
        self.shuffle()

    def shuffle(self):
        shuffle(self.cards)

    def get_a_card(self):
        return self.cards.pop()

    # returns list of Cards
    def deal(self, number_of_cards):
        hand = []
        for i in range(number_of_cards):
            hand.append(self.cards.pop())
        return hand
