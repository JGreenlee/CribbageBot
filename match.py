from asyncinit import asyncinit
from discord import TextChannel

from game import Game


@asyncinit
class Match:

    async def __init__(self, bot, channel: TextChannel, players):
        self.bot = bot
        self.channel = channel
        self.players = players
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

        self.game = None

        print("Welcome to Cribbage", players, "!")

    async def award_points(self, points, player_name, reason):
        await self.channel.send(str(points) + " point" + ("s" if points > 1 else "") +
                                " to " + player_name + " for " + reason)
        self.scores[player_name] += points
        for player in self.players:
            if self.scores[player] > 120:
                self.winner = player
                raise GameWon

    async def begin(self):
        try:
            await self.run_games(self.players.copy())
        except GameWon:
            await self.channel.send("Game over! " + self.winner + " wins!")
            return

    async def run_games(self, game_players):
        game_players.append(game_players.pop(0))  # rotate players
        self.game = await Game(self.bot, self, game_players, self.run_games)


class GameWon(Exception):
    pass
