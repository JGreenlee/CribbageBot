from deck import Deck
from hand import Hand
from pegging import Pegging

class Game:

    def __init__(self, p1, p2, p3=0):

        self.three_players = p3 != 0

        deck = Deck()
        deck.shuffle()

        if self.three_players:
            one = Hand(p1, deck.deal(5))
            two = Hand(p2, deck.deal(5))
            three = Hand(p3, deck.deal(5))
            crib = Hand(deck.deal(1))
        else:
            one = Hand(p1, deck.deal(6))
            # one = Hand([Card(0, 5), Card(1, 5), Card(2, 5), Card(3, 11)])
            two = Hand(p2, deck.deal(6))
            three = 0
            crib = Hand()

        one.show_hand("one")
        two.show_hand("two")
        if self.three_players:
            three.show_hand("three")

        if self.three_players:
            resp = input(one.name + "  -  Select 1 cards to get rid of:")
            first = one.cards.pop(int(resp))
            crib.cards.append(first)

            resp = input("\n\n" + two.name + "  -  Select 1 cards to get rid of:")
            first = two.cards.pop(int(resp))
            crib.cards.append(first)

            resp = input("\n\n" + three.name + "  -  Select 1 cards to get rid of:")
            first = three.cards.pop(int(resp))
            crib.cards.append(first)
        else:
            resp = input(one.name + "  -  Select 1 cards to get rid of:")
            resp = resp.split(",")
            first, second = one.cards.pop(int(resp[1])), one.cards.pop(int(resp[0]))
            crib.cards.append(first), crib.cards.append(second)

            resp = input("\n\n" + two.name + "  -  Select 1 cards to get rid of:")
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

        if three:
            players = [one, two, three]
        else:
            players = [one, two]

        for hand in players:
            hand.pegging_cards = hand.cards.copy()

        Pegging(players)

        # counting hands

        print(one.name + "'s hand:")
        print(one)
        print("*", end="", flush=True), print(starter)
        one.fifteens(starter)
        one.pairs(starter)
        one.straights(starter)
        one.flush_and_nobs(starter)
        print(str(one.score) + " points!")

        print("\n\n")

        print(two.name + "'s hand:")
        print(two)
        print("*", end="", flush=True), print(starter)
        two.fifteens(starter)
        two.pairs(starter)
        two.straights(starter)
        two.flush_and_nobs(starter)
        print(str(two.score) + " points!")

        if self.three_players:
            print("\n\n")

            print(three.name + "'s hand:")
            print(three)
            print("*", end="", flush=True), print(starter)
            three.fifteens(starter)
            three.pairs(starter)
            three.straights(starter)
            three.flush_and_nobs(starter)
            print(str(three.score) + " points!")

        print("\n\n")

        print("The Crib:")
        print(crib)
        print("*", end="", flush=True), print(starter)
        crib.fifteens(starter)
        crib.pairs(starter)
        crib.straights(starter)
        crib.flush_and_nobs(starter)
        print(str(crib.score) + " points!")
