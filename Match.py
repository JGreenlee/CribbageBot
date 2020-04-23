from game import Game


class Match:

    def __init__(self, players):
        self.players = players
        self.game_over = False
        if len(players) > 2:
            self.three_players = True
            self.scores = {
                players[0]: 0,
                players[1]: 0,
                players[2]: 0
            }
        else:
            self.three_players = False
            self.scores = {
                players[0]: 0,
                players[1]: 0
            }

        while not self.game_over:
            Game(self, players)

    def award_points(self, points, player, reason):
        print(str(points) + " point" + ("s" if points > 1 else "") + " to " + player.name + " for " + reason)
        self.scores[player.name] += points
        for player in self.players:
            if self.scores[player] > 120:
                self.game_over = True
                winner = player


Match(["p1", "p2", "p3"])
