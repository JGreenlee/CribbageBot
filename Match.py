from game import Game


class Match:
    P1_SCORE, P2_SCORE, P3_SCORE = 0, 0, 0
    THREE_PLAYERS = False

    def __init__(self, three_players=False):
        Game(three_players)


Match()
