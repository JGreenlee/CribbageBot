from deck import Deck
from hand import Hand
from card import Card

class Game:

    THREE_PLAYERS = False

    def __init__(self):

        deck = Deck()
        deck.shuffle()

        if self.THREE_PLAYERS:
            one = Hand(deck.deal(5))
            two = Hand(deck.deal(5))
            three = Hand(deck.deal(5))
        else:
            # one = Hand(deck.deal(6))
            one = Hand([Card(0, 5), Card(1, 5), Card(2, 5), Card(3, 11)])
            two = Hand(deck.deal(6))


        print(one)
        # starter = deck.deal(1)[0]
        starter = Card(3, 5)
        print("*", end="", flush=True), print(starter)
        one.fifteens(starter)
        one.pairs(starter)
        one.straights(starter)
        one.flush_and_nobs(starter)
        print(one.score)
        # print(two)

        one.show_hand(starter)

Game()