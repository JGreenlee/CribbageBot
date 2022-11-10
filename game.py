from typing import List
from asyncinit import asyncinit

from deck import Deck
from hand import Hand
from pegging import Pegging


@asyncinit
class Game:

    async def __init__(self, bot, match, players, callback_on_game_end):

        self.bot = bot
        self.match = match
        self.players = players
        self.callback_on_game_end = callback_on_game_end

        self.num_players = len(players)
        self.deck = Deck()
        self.hands: List[Hand] = []
        self.pegging = None

        await self.deal_hands(players)

    async def begin(self):
        starter = self.deck.deal(1)[0]
        await self.match.channel.send("The starter is: " + str(starter))

        for hand in self.hands:
            hand.pegging_cards = hand.cards.copy()
        self.pegging = await Pegging(self.match, self.hands,
                                     self.count_hands(starter))

    async def deal_hands(self, players):
        num_cards = 6 if self.num_players == 2 else 5
        for p in players:
            self.hands.append(Hand(self.deck.deal(num_cards), p))
            # if odd num (3 players), deal one to the crib, else deal 0
            self.crib = Hand(self.deck.deal(self.num_players % 2))

    # return true if begin
    async def discard(self, user_name, card_index):
        hand = next(h for h in self.hands if h.name == user_name)
        if len(hand.cards) > 4:
            c = hand.dealt_cards[card_index]
            hand.cards.remove(c)
            self.crib.cards.append(c)
            print('discarded the', card_index,
                  'card from', user_name, '\'s hand')

        if (len(self.crib.cards) == 4):
            await self.begin()
            return True

        return False

    async def count_hands(self, starter):

        for h in self.hands:
            await self.match.channel.send("Counting " + h.name + "'s hand..." +
                                          '\n\n' + str(h) + '\n\n' + str(starter))
            h.fifteens(starter)
            h.pairs(starter)
            h.runs(starter)
            h.flush_and_nobs(starter)
            await self.match.award_points(h.score, h.name, "their hand.")

        crib_owner = self.hands[len(self.hands)-1].name

        await self.match.channel.send("Counting " + crib_owner + "'s crib..." +
                                      '\n\n' + str(self.crib) + '\n\n' + str(starter))

        self.crib.fifteens(starter)
        self.crib.pairs(starter)
        self.crib.runs(starter)
        self.crib.flush_and_nobs(starter)
        await self.match.award_points(self.crib.score, crib_owner, "their crib.")
        self.callback_on_game_end(self.players)
