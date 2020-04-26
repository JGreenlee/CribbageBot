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

        print("Welcome to Cribbage", players, "!")

        game_players = players.copy()
        try:
            while not self.game_over:
                Game(self, game_players)
                game_players.append(game_players.pop(0))
        except GameWon:
            print("GAME OVER: " + self.winner + " wins!")

    def award_points(self, points, player, reason):
        print(str(points) + " point" + ("s" if points > 1 else "") + " to " + player.name + " for " + reason)
        self.scores[player.name] += points
        for player in self.players:
            if self.scores[player] > 120:
                self.winner = player
                raise GameWon


class GameWon(Exception):
    pass


Match(["p1", "p2", "p3"])
