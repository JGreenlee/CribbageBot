from asyncinit import asyncinit


@asyncinit
class Pegging:

    async def __init__(self, match, players, callback_on_pegging_end):

        self.match = match
        self.players = players
        self.callback_on_pegging_end = callback_on_pegging_end

        self.pegging_count = 0
        self.to_play = 0
        self.laZst_played = -1
        last = 0
        self.last_six = []

        # while players[0].has_cards() or players[1].has_cards() or players[len(players) - 1].has_cards():

        #     if self.last_played + 1 < len(players):
        #         self.to_play = self.last_played + 1
        #     else:
        #         self.to_play = 0

        #     # if to_play can play
        #     if self.pegging_count + players[self.to_play].pegging_cards[0].pegging_value <= 31:
        #         resp = input(str(self.pegging_count) + " to " +
        #                      players[self.to_play].name + "  -  Select a card to play:")
        #         just_played = players[self.to_play].pegging_cards.pop(
        #             int(resp))
        #         self.pegging_count += just_played.pegging_value
        #         print(players[self.to_play].name + " played " + just_played.get_value_name() + ". Total is " + str(
        #             self.pegging_count))
        #         pairs_points = self.pairs(self.last_six, just_played)
        #         if pairs_points:
        #             match.award_points(
        #                 pairs_points, players[self.to_play].name, "pegging pairs.")
        #         runs_points = self.runs(self.last_six, just_played)
        #         if runs_points:
        #             match.award_points(
        #                 runs_points, players[self.to_play].name, "pegging a run of " + str(runs_points) + ".")
        #         self.last_six.append(just_played)
        #         if len(self.last_six) > 6:
        #             self.last_six.pop(0)
        #         if self.pegging_count == 15:
        #             self.match.award_points(
        #                 2, players[self.to_play].name, "for landing on 15.")
        #         elif self.pegging_count == 31:
        #             self.match.award_points(
        #                 2, players[self.to_play].name, "for landing on 31.")
        #             self.pegging_count = 0
        #             self.last_six.clear()
        #         self.last_played = self.to_play
        #     else:
        #         next_player = players[self.get_next_player(self.to_play)]
        #         next_next_player = players[self.get_next_player(
        #             self.get_next_player(self.to_play))]
        #         # if no one can play
        #         if len(next_player.pegging_cards) < 1 \
        #                 or self.pegging_count + next_player.pegging_cards[0].pegging_value > 31 \
        #                 and len(next_next_player.pegging_cards) < 1 \
        #                 or self.pegging_count + next_next_player.pegging_cards[0].pegging_value > 31:
        #             self.match.award_points(
        #                 1, players[self.last_played].name, "for \"go.\"")
        #             self.pegging_count = 0
        #             self.last_six.clear()
        #         else:
        #             # TODO fix someone can play bug
        #             print("someone can play")
        #             raise Exception

        # # AWARD POINTS - for last card
        # self.match.award_points(
        #     1, players[self.last_played].name, "for last card.")

    # card_index of None means you're saying 'go'
    async def play_card(self, player_name, card_index):
        player = next(p for p in self.players if p.name == player_name)
        player_index = self.players.index(player)
        if (player_index == self.to_play):
            if card_index is None:
                # 'go', next player's turn
                if self.last_played + 1 < len(self.players):
                    self.to_play = self.last_played + 1
                else:
                    self.to_play = 0
                return True
            if self.pegging_count + player.pegging_cards[card_index].pegging_value <= 31:
                just_played = player.pegging_cards.pop(card_index)
                self.pegging_count += just_played.pegging_value
                print(player.name + " played " + just_played.get_value_name() + ". Total is " + str(
                    self.pegging_count))
                pairs_points = self.pairs(self.last_six, just_played)
                if pairs_points:
                    await self.match.award_points(
                        pairs_points, player.name, "pegging pairs.")
                runs_points = self.runs(self.last_six, just_played)
                if runs_points:
                    await self.match.award_points(
                        runs_points, player.name, "pegging a run of " + str(runs_points) + ".")
                self.last_six.append(just_played)
                if len(self.last_six) > 6:
                    self.last_six.pop(0)
                if self.pegging_count == 15:
                    await self.match.award_points(
                        2, player.name, "for landing on 15.")
                elif self.pegging_count == 31:
                    await self.match.award_points(
                        2, player.name, "for landing on 31.")
                    self.pegging_count = 0
                    self.last_six.clear()
                self.last_played = player_index

                # if no one has cards, award points for last card
                if not any(p.has_cards() for p in self.players):
                    await self.match.award_points(
                        1, self.players[self.last_played].name, "for last card.")
                    # no cards left, so we're done
                    await self.callback_on_pegging_end()
                    return

                # next player's turn
                if self.last_played + 1 < len(self.players):
                    self.to_play = self.last_played + 1
                else:
                    self.to_play = 0
                return True
            else:
                # you can't play this card, it would go over 31
                return False
        else:
            # not your turn
            return False

    def can_play(self, player_name):
        player = next(p for p in self.players if p.name == player_name)
        player_index = self.players.index(player)
        if (player.has_cards() and self.pegging_count + player.pegging_cards[0] <= 31):
            return True
        else:
            return False

    def get_next_player(self, current_player):
        if current_player + 1 < len(self.players):
            next_player = current_player + 1
        else:
            next_player = 0
        return next_player

    @staticmethod
    def is_run(cards, card=0):
        copy = cards.copy()
        if card:
            copy.append(card)
        sorted_cards = sorted(copy)
        for x in range(len(sorted_cards) - 1):
            if sorted_cards[x + 1].value != sorted_cards[x].value + 1:
                return False
        return True

    @staticmethod
    def runs(last_six, last):
        # check for run of x
        for x in range(7, 2, -1):  # at most, you can peg a run of 7
            if len(last_six) - x + 1 >= 0:
                if Pegging.is_run(last_six[len(last_six) - x + 1:], last):  # type: ignore
                    return x
        return 0

    @staticmethod
    def pairs(last_six, last):
        total = 0
        if len(last_six) > 0 and last.value == last_six[len(last_six) - 1].value:
            if len(last_six) > 1 and last.value == last_six[len(last_six) - 2].value:
                if len(last_six) > 2 and last.value == last_six[len(last_six) - 3].value:
                    total = 12
                else:
                    total = 6
            else:
                total = 2
        return total
