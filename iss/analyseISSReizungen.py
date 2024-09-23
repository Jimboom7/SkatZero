import random
import numpy as np

from iss.SkatMatch import SkatMatch
from skatzero.evaluation.utils import swap_colors
from skatzero.game.player import Player
from skatzero.game.dealer import Dealer

def parse_bid(bid_value, pos, bids, bid_jacks):
    d_bids = [18, 27, 45]
    h_bids = [20, 30, 40, 50]
    s_bids = [22, 33, 44, 55]
    c_bids = [24, 36, 48, 60]
    n_bids = [23, 35, 46, 59]

    if bid_value in d_bids:
        bids[pos]['D'] = 1
        if bid_value != 18:
            bid_jacks[pos] = int(bid_value / 9) - 1
    elif bid_value in h_bids:
        bids[pos]['H'] = 1
        bid_jacks[pos] = int(bid_value / 10) - 1
    elif bid_value in s_bids:
        bids[pos]['S'] = 1
        bid_jacks[pos] = int(bid_value / 11) - 1
    elif bid_value in c_bids:
        bids[pos]['C'] = 1
        bid_jacks[pos] = int(bid_value / 12) - 1
    elif bid_value in n_bids:
        bids[pos]['N'] = 1

    return bids, bid_jacks

def print_info(match, gametype):
    if match.alleinspielerInd not in [0, 1, 2] or match.playerNames[match.alleinspielerInd] == 'kermit':
        return -1
    kermit_id=-1
    if match.playerNames[0] == 'kermit':
        kermit_id = 0
    if match.playerNames[1] == 'kermit':
        kermit_id = 1
    # if match.playerNames[2] == 'kermit':
    #     kermit_id = 2
    if kermit_id == -1:
        return -1

    dealer = Dealer(np.random.RandomState())
    players = [{}]
    players[0] = Player(1)
    players[0].current_hand = match.cards['kermit']
    dealer.set_bids(players)

    bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    bid_jacks = [0, 0, 0]
    bids, bid_jacks = parse_bid(match.maxReizungen[kermit_id], 1, bids, bid_jacks)

    if bids[1]['N'] == 1:
        return -1

    if dealer.bids[1] == bids[1] and dealer.bid_jacks[1] == bid_jacks[1]:
        print("Korrekt!")
        return 1

    print(match.cards)
    print(dealer.bids[1])
    print(dealer.bid_jacks[1])
    print(bids[1])
    print(bid_jacks[1])
    print(match.maxReizungen[kermit_id])

    return 0


def analyze_reizungen(logFilePath):
    cards = []
    print('Reading file...')
    i = 0
    ges = 0
    hit = 0
    for line in reversed(list(open(logFilePath))):
        try:
            match = SkatMatch(line)
            res = print_info(match, 'D')
            if res >= 0:
                ges += 1
                if res == 1:
                    hit += 1
            i += 1
            if i > 10000:
                break
        except:
            pass

    print("Result: " + str(hit*100/ges))

    return cards


if __name__ == '__main__':
    # Parameter
    issLogFilePath = 'C:/Users/janvo/Desktop/Skat/skatgame-games-07-2024/skatgame-games-07-2024.sgf'

    analyze_reizungen(issLogFilePath)