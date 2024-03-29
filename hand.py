from typing import List
from PIL import Image

from card import Card


class Hand:
    def __init__(self, cards: List[Card] = [], name: str = ''):
        self.name = name
        self.cards: List[Card] = sorted(cards)
        self.dealt_cards = self.cards.copy()
        self.pegging_cards = []
        self.score = 0

    def toss(self, index):
        card = self.cards[index]
        del self.cards[index]
        return card

    def has_cards(self):
        if len(self.pegging_cards) > 0:
            return True

    def fifteens(self, starter, x=0, total=0):
        while x < 5:
            if x == 4:
                j = starter
            else:
                j = self.cards[x]
            # add j to stack
            if j.value > 9:
                subtotal = total + 10
            else:
                subtotal = total + j.value

            if subtotal == 15:
                self.score += 2
                # confirm stack as a 15
            elif subtotal < 15:
                self.fifteens(starter, x + 1, subtotal)
            # else clear stack
            x += 1

    def pairs(self, starter):

        for x in range(5):
            for y in range(5):
                if x == 4:
                    i = starter
                else:
                    i = self.cards[x]
                if y == 4:
                    j = starter
                else:
                    j = self.cards[y]
                if j != i and i.value == j.value:
                    self.score += 1

    def runs(self, starter):
        fullhand = self.cards.copy()
        fullhand.append(starter)

        fullhand = sorted(fullhand)

        double = 0
        triple = False
        streak = 1

        for x in range(4):
            if fullhand[x + 1].value == fullhand[x].value:
                double = fullhand[x].value
                if fullhand[x].value == double:
                    triple = True
            elif fullhand[x + 1].value == fullhand[x].value + 1:
                streak += 1
            else:
                if streak > 2:
                    if triple:
                        self.score += streak * 3
                    elif double != 0:
                        self.score += streak * 2
                    else:
                        self.score += streak

                streak = 1
                double = 0

        if streak > 2:
            if triple:
                self.score += streak * 3
            elif double != 0:
                self.score += streak * 2
            else:
                self.score += streak

    def flush_and_nobs(self, starter):

        # flush
        if self.cards[0].get_suit_name() == \
                self.cards[1].get_suit_name() == \
                self.cards[2].get_suit_name() == \
                self.cards[3].get_suit_name():
            self.score += 4
            if self.cards[0].get_suit_name() == starter.get_suit_name():
                self.score += 1

        # nobs
        starter_suit = starter.get_suit_name()
        for i in range(4):
            if self.cards[i].value == 11 and self.cards[i].get_suit_name() == starter_suit:
                self.score += 1

    # returns image showing cards in hand
    def show_hand(self, filename, starter=None, pegging=False):

        if starter != None:
            fullhand = self.pegging_cards if pegging else self.cards.copy()
            fullhand.append(starter)
        else:
            fullhand = self.pegging_cards if pegging else self.cards
        result = Image.new("RGBA", (196 * len(fullhand), 300))

        for i in range(len(fullhand)):
            img = Image.open("cards_pngs/" + fullhand[i].filename() + ".bmp")
            x, y = img.size
            result.paste(img, (x * i, 0))
        return result

    def __repr__(self):
        ret = ""
        for x in self.cards:
            ret += "\n" + x.__repr__()
        return ret
