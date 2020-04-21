class Pegging:

    def __init__(self, players):

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
                # TODO pegging straights
                last_six.append(just_played)
                pegging_count += just_played.pegging_value
                if pegging_count == 15:
                    # AWARD POINTS - landing on 15
                    print("2 point to " + players[last_played].name + " for landing on 15.")
                    players[last_played].score += 2
                elif pegging_count == 31:
                    # AWARD POINTS - landing on 31
                    print("2 point to " + players[last_played].name + " for landing on 31.")
                    players[last_played].score += 2
                    pegging_count = 0
                print(players[to_play].name + " played " + just_played.get_value_name() + ". Total is " + str(pegging_count))
                last_played = to_play
            else:
                next_player = players[self.get_next_player(to_play)]
                next_next_player = players[self.get_next_player(self.get_next_player(to_play))]
                # if no one can play
                if len(next_player.pegging_cards) < 1 \
                        or pegging_count + next_player.pegging_cards[0].pegging_value > 31 \
                        and len(next_next_player.pegging_cards) < 1 \
                        or pegging_count + next_next_player.pegging_cards[0].pegging_value > 31:
                    # AWARD POINTS - for "go"
                    print("1 point to " + players[last_played].name + " for \"go.\"")
                    players[last_played].score += 1
                    pegging_count = 0

        # AWARD POINTS - for last card
        print("1 point to " + players[last_played].name + " for last card.")
        players[last_played].score += 1

    def get_next_player(self, current_player):
        if current_player + 1 < len(self.players):
            next_player = current_player + 1
        else:
            next_player = 0
        return next_player

    def runs(self, last_six, last):
        return
        # from hand.py
        # for x in range(4):
        #     if fullhand[x + 1].value == fullhand[x].value:
        #         double = fullhand[x].value
        #         if fullhand[x].value == double:
        #             triple = True
        #     elif fullhand[x + 1].value == fullhand[x].value + 1:
        #         streak += 1
        #     else:
        #         if streak > 2:
        #             if triple:
        #                 self.score += streak * 3
        #             elif double != 0:
        #                 self.score += streak * 2
        #             else:
        #                 self.score += streak
        #
        #         streak = 1
        #         double = 0


def pairs(self, last_six, last):
    total = 0
    if last.value == last_six[5].value:
        if last.value == last_six[4].value:
            if last.value == last_six[4].value:
                total = 12
            else:
                total = 6
        else:
            total = 2
    return total
