from deck import Deck
from hand import Hand


class Game:

    def __init__(self, three_players):

        self.three_players = three_players

        deck = Deck()
        deck.shuffle()

        if self.three_players:
            one = Hand(deck.deal(5))
            two = Hand(deck.deal(5))
            three = Hand(deck.deal(5))
            crib = Hand(deck.deal(1))
        else:
            one = Hand(deck.deal(6))
            # one = Hand([Card(0, 5), Card(1, 5), Card(2, 5), Card(3, 11)])
            two = Hand(deck.deal(6))
            crib = Hand()

        one.show_hand("one")
        two.show_hand("two")
        if self.three_players:
            three.show_hand("three")

        if self.three_players:
            resp = input("Player One  -  Select 1 cards to get rid of:")
            first = one.cards.pop(int(resp))
            crib.cards.append(first)

            resp = input("\n\nPlayer Two  -  Select 1 cards to get rid of:")
            first = two.cards.pop(int(resp))
            crib.cards.append(first)

            resp = input("\n\nPlayer Three  -  Select 1 cards to get rid of:")
            first = three.cards.pop(int(resp))
            crib.cards.append(first)
        else:
            resp = input("Player One  -  Select 2 cards to get rid of:")
            resp = resp.split(",")
            first, second = one.cards.pop(int(resp[1])), one.cards.pop(int(resp[0]))
            crib.cards.append(first), crib.cards.append(second)

            resp = input("\n\nPlayer Two  -  Select 2 cards to get rid of:")
            resp = resp.split(",")
            first, second = two.cards.pop(int(resp[1])), two.cards.pop(int(resp[0]))
            crib.cards.append(first), crib.cards.append(first)

        print("\n\n")

        starter = deck.deal(1)[0]
        # starter = Card(3, 5)
        print("The starter card is:")
        print(starter)

        print("\n\n")

        # TODO pegging

        print("Player One:")
        print(one)
        print("*", end="", flush=True), print(starter)
        one.fifteens(starter)
        one.pairs(starter)
        one.straights(starter)
        one.flush_and_nobs(starter)
        print(str(one.score) + " points!")

        print("\n\n")

        print("Player Two:")
        print(two)
        print("*", end="", flush=True), print(starter)
        two.fifteens(starter)
        two.pairs(starter)
        two.straights(starter)
        two.flush_and_nobs(starter)
        print(str(two.score) + " points!")

        if three_players:
            print("\n\n")

            print("Player Three:")
            print(three)
            print("*", end="", flush=True), print(starter)
            three.fifteens(starter)
            three.pairs(starter)
            three.straights(starter)
            three.flush_and_nobs(starter)
            print(str(three.score) + " points!")

        print("\n\n")

        print("Crib:")
        print(crib)
        print("*", end="", flush=True), print(starter)
        crib.fifteens(starter)
        crib.pairs(starter)
        crib.straights(starter)
        crib.flush_and_nobs(starter)
        print(str(crib.score) + " points!")