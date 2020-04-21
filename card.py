class Card:

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        if value > 9:
            self.pegging_value = 10
        else:
            self.pegging_value = value

    # suits are 0-3
    def get_suit_name(self):
        if self.suit == 0:
            return "hearts"
        elif self.suit == 1:
            return "clubs"
        elif self.suit == 2:
            return "diamonds"
        elif self.suit == 3:
            return "spades"
        else:
            raise Exception("card has undefined suit")

    # values are 1-13
    def get_value_name(self):
        if self.value == 1:
            return "ace"
        elif self.value < 11:
            return str(self.value)
        elif self.value == 11:
            return "jack"
        elif self.value == 12:
            return "queen"
        elif self.value == 13:
            return "king"
        else:
            raise Exception("card has undefined value")

    def __repr__(self):
        return self.get_value_name() + " of " + self.get_suit_name()

    def __lt__(self, other):
        if self.value < other.value:
            return True

    def __gt__(self, other):
        if self.value > other.value:
            return True
