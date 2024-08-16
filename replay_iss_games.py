"""
Read a iss.log file.
Deals the exact same cards and lets AI agents play them.
"""
from iss.SkatMatch import SkatMatch
from skatzero.evaluation.simulation import load_model, set_seed
from skatzero.evaluation.eval_env import EvalEnv
from skatzero.evaluation.utils import swap_bids, swap_colors
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

def set_dealer_data(match, gametype):
    dealer = Dealer(None)
    dealer.starting_player = (3 - match.alleinspielerInd) % 3

    dealer.deck = match.cards[match.playerNames[match.alleinspielerInd]]
    dealer.deck += match.originalSkat
    dealer.deck = [a for a in dealer.deck if a not in match.gedrueckt_cards]
    dealer.deck += match.cards[match.playerNames[(match.alleinspielerInd + 1) % 3]]
    dealer.deck += match.cards[match.playerNames[(match.alleinspielerInd + 2) % 3]]
    dealer.deck += match.gedrueckt_cards

    dealer.bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    dealer.bid_jacks = [0, 0, 0]
    dealer.bids, dealer.bid_jacks = parse_bid(match.maxReizungen[(match.alleinspielerInd + 1) % 3], 1, dealer.bids, dealer.bid_jacks)
    dealer.bids, dealer.bid_jacks = parse_bid(match.maxReizungen[(match.alleinspielerInd + 2) % 3], 2, dealer.bids, dealer.bid_jacks)

    if gametype == 'D' and match.gameType[0] != 'D':
        dealer.deck = swap_colors(dealer.deck, 'D', match.gameType[0])
        dealer.bids[0] = swap_bids(dealer.bids[0], 'D', match.gameType[0])
        dealer.bids[1] = swap_bids(dealer.bids[1], 'D', match.gameType[0])
        dealer.bids[2] = swap_bids(dealer.bids[2], 'D', match.gameType[0])

    dealer.blind_hand = match.is_hand
    dealer.open_hand = False # Ignore open Null games

    #print(match.alleinspielerInd)
    #print(match.gameType)
    #print(dealer.deck)
    #print(dealer.bids)
    #print(dealer.blind_hand)

    return dealer

def get_reward(score, is_hand, base_value):
    if score == 120:
        return ((4 + is_hand) * base_value) + 50
    elif score >= 90:
        return ((3 + is_hand) * base_value) + 50
    elif score > 60:
        return ((2 + is_hand) * base_value) + 50
    elif score == 0:
        return (((-4 - is_hand) * 2) * base_value) - 50 - 40
    elif score <= 30:
        return (((-3 - is_hand) * 2) * base_value) - 50 - 40
    elif score <= 60:
        return (((-2 - is_hand) * 2) * base_value) - 50 - 40

if __name__ == '__main__':

    seed = 42
    set_seed(seed)

    gametype = 'D'
    name = 'Hubert47'

    with open('C:/Users/janvo/Desktop/log.txt', encoding='utf-8') as fRaw:

        line = fRaw.readline()

        dealers = []

        points = 0

        while line:
            try:
                match = SkatMatch(line)
                if not match.eingepasst and (gametype == match.gameType[0] or (gametype == 'D' and match.gameType[0] in ['H', 'S', 'C'])):
                    if match.playerNames[match.alleinspielerInd] == name or match.playerNames[match.alleinspielerInd] == name + ':2':
                        dealer = set_dealer_data(match, gametype)
                        dealers.append(dealer)
                        points += get_reward(match.stichPoints, match.is_hand, 10 if gametype == 'D' else 24)
                        #print(line)
                        #print(get_reward(match.stichPoints, match.is_hand, 10))
            except:
                pass
            line = fRaw.readline()
        print("Anzahl Spiele: " + str(len(dealers)))
        print(points / len(dealers))

    env = EvalEnv(seed=seed, gametype=gametype, lstm=[True, True, True], dealers=dealers)

    agent_0 = load_model('models/latest/' + env.game.gametype + '_0.pth')
    agent_1 = load_model('models/latest/' + env.game.gametype + '_1.pth')
    agent_2 = load_model('models/latest/' + env.game.gametype + '_2.pth')

    #agent_0 = load_model('models/checkpoints/skat_lstm_D/0_9980.pth')
    #agent_1 = load_model('models/checkpoints/skat_lstm_D/1_13100.pth')
    #agent_2 = load_model('models/checkpoints/skat_lstm_D/2_13100.pth')

    #agent_0 = load_model('models/checkpoints/skat_lstm_G/0_10000.pth')
    #agent_1 = load_model('models/checkpoints/skat_lstm_G/1_10660.pth')
    #agent_2 = load_model('models/checkpoints/skat_lstm_G/2_10660.pth')

    env.set_agents([
        agent_0,
        agent_1,
        agent_2,
    ])

    points = 0
    for d in dealers:
        trajectories, rewards = env.run(is_training=False, verbose=0)
        points += rewards[0]
        #print(rewards[0])
    print(points / len(dealers))
