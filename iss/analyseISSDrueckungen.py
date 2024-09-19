import random
import numpy as np

from iss.SkatMatch import SkatMatch
from skatzero.game.player import Player
from skatzero.game.dealer import Dealer


def analyze_drueckungen(logFilePath):
    cards = []
    print('Reading file...')
    with open(logFilePath) as fRaw:

        line = fRaw.readline()

        hit = 0
        hit2 = 0
        gesamt = 0
        while line:
            try:
                match = SkatMatch(line)
                hit, hit2, gesamt = print_info(match, hit, hit2, gesamt)
            except:
                pass
            line = fRaw.readline()
    return cards

d = Dealer(np.random.RandomState())
players = [{},{},{}]
players[0] = Player(0)
players[1] = Player(1)
players[2] = Player(2)

def print_info(match, hit, hit2, gesamt):
    gametype = 'N'
    if((match.alleinspielerName != 'kermit' and match.alleinspielerName != 'kermit:2' and
        match.alleinspielerName != 'zoot' and match.alleinspielerName != 'zoot:2'
        and match.alleinspielerName != 'theCount' and match.alleinspielerName != 'theCount:2') and match.gameType == gametype):
        # print(match.gameType)
        print(match.cards[match.alleinspielerName] + match.originalSkat)
        # print(', '.join([format_card(card) for card in match.cards[match.alleinspielerName] + match.originalSkat]))
        #print(match.gedrueckt_cards)
        players[0].current_hand = match.cards[match.alleinspielerName]
        #random.shuffle(players[0].current_hand)
        d.skat = match.originalSkat
        #d.swap_suit_for_D_game(players, 'C')
        #match.gedrueckt_cards = swap_colors(match.gedrueckt_cards, 'D', 'C')
        x = 0
        for _ in range(1):
            d.pickup_skat(players)
            if match.gedrueckt_cards[0] in d.skat and match.gedrueckt_cards[1] in d.skat:
                hit += 1
                x += 1
            if match.gedrueckt_cards[0] in d.skat or match.gedrueckt_cards[1] in d.skat:
                hit2 += 1
            gesamt += 1
        if x < 1:
            print("XXXXXXXXXXXXXXXXXXXXXXXXX")
        print(match.gedrueckt_cards)
        print("both: " + str((hit * 100)/gesamt))
        print("one:  " + str((hit2 * 100)/gesamt))
    return hit, hit2, gesamt


if __name__ == '__main__':
    # Parameter
    # issLogFilePath = 'C:/Users/janvo/Desktop/Skat/ISS-Bot/logs/log_all.txt'
    issLogFilePath = 'C:/Users/janvo/Desktop/Skat/skatgame-games-07-2024/high_elo_N.txt'

    analyze_drueckungen(issLogFilePath)
