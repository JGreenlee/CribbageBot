class Pegging:

    def __init__(self, match, players):

        self.match = match
        self.players = players

        pegging_count = 0
        to_play = 0
        last_played = -1
        last = 0
        last_six = []

        while players[0].has_cards() or players[1].has_cards() or players[len(players) - 1].has_cards():

            if last_played + 1 < len(players):
                to_play = last_played + 1
            else:
                to_play = 0

            # if to_play can play
            if pegging_count + players[to_play].pegging_cards[0].pegging_value <= 31:
                resp = input(str(pegging_count) + " to " + players[to_play].name + "  -  Select a card to play:")
                just_played = players[to_play].pegging_cards.pop(int(resp))
                pegging_count += just_played.pegging_value
                print(players[to_play].name + " played " + just_played.get_value_name() + ". Total is " + str(
                    pegging_count))
                pairs_points = self.pairs(last_six, just_played)
                if pairs_points:
                    match.award_points(pairs_points, players[to_play], "pegging pairs.")
                runs_points = self.runs(last_six, just_played)
                if runs_points:
                    match.award_points(runs_points, players[to_play], "pegging a run of " + str(runs_points) + ".")
                last_six.append(just_played)
                if len(last_six) > 6:
                    last_six.pop(0)
                if pegging_count == 15:
                    self.match.award_points(2, players[to_play], "for landing on 15.")
                elif pegging_count == 31:
                    self.match.award_points(2, players[to_play], "for landing on 31.")
                    pegging_count = 0
                    last_six.clear()
                last_played = to_play
            else:
                next_player = players[self.get_next_player(to_play)]
                next_next_player = players[self.get_next_player(self.get_next_player(to_play))]
                # if no one can play
                if len(next_player.pegging_cards) < 1 \
                        or pegging_count + next_player.pegging_cards[0].pegging_value > 31 \
                        and len(next_next_player.pegging_cards) < 1 \
                        or pegging_count + next_next_player.pegging_cards[0].pegging_value > 31:
                    self.match.award_points(1, players[last_played], "for \"go.\"")
                    pegging_count = 0
                    last_six.clear()
                else:
                    # TODO fix someone can play bug
                    print("someone can play")
                    raise Exception

        # AWARD POINTS - for last card
        self.match.award_points(1, players[last_played], "for last card.")

    def get_next_player(self, current_player):
        if current_player + 1 < len(self.players):
            next_player = current_player + 1
        else:
            next_player = 0
        return next_player

    @staticmethod
    def runs(last_six, last):
        # check for run of x
        for x in range(7, 2, -1):  # at most, you can peg a run of 7
            if len(last_six) - x + 1 >= 0:
                if Pegging.is_run(last_six[len(last_six) - x + 1:], last):
                    return x
        return 0

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