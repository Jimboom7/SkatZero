from bidding.bidder import Bidder
from iss.SkatMatch import SkatMatch
from iss_api import prepare_env
from skatzero.game.utils import init_32_deck
from skatzero.test.utils import available_actions


def getHandsFromLogFile(logFilePath):
    cards = []
    reiz = []
    outcomes = []
    print('Reading file...')
    with open(logFilePath) as fRaw:

        line = fRaw.readline()

        while line:
            try:
                match = SkatMatch(line)
                cards.append(match.cards)
                if not match.eingepasst:
                    reiz.append(max(match.maxReizungen[(match.alleinspielerInd + 1) % 3], match.maxReizungen[(match.alleinspielerInd + 2) % 3], 18))
                else:
                    reiz.append(18)
                if not match.eingepasst and match.gameType[0] != 'N' and match.alleinspielerName == 'Hubert47':
                    outcomes.append(match.stichPoints > 60)
                else:
                    outcomes.append(-1)
            except:
                pass
            line = fRaw.readline()
    return cards, reiz, outcomes

def analyseHand(cards, reiz=18):
    _, env, raw_state = prepare_env()

    raw_state['current_hand'] = cards
    others_cards = init_32_deck()
    for c in raw_state['current_hand']:
        others_cards.remove(c)
    raw_state['others_hand'] = others_cards
    raw_state['skat'] = []
    raw_state['actions'] = available_actions(raw_state['current_hand'])

    bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    bid_jacks = [0, 0, 0]
    penalties = {'D': 25, 'G': 40, 'N': 0, 'NO': 0}

    raw_state['bids'] = bids
    raw_state['bid_jacks'] = bid_jacks

    bidder = Bidder(env, raw_state, 0, penalties)
    
    hand_estimates = bidder.get_blind_hand_values()
    return max(hand_estimates), 0
    # for _ in range(10):
    #     mean_estimates, bid_value_dict = bidder.update_value_estimates(5)
    # return bid_value_dict[18], bid_value_dict[reiz]
    

if __name__ == '__main__':
    # Parameter
    issLogFilePath = 'C:/Users/janvo/Desktop/Skat/ISS-Bot/log.txt'

    cards, reiz, outcomes = getHandsFromLogFile(issLogFilePath)

    score = 0
    i = 0
    for card in cards:
        val, actual_val = analyseHand(card["Hubert47"], reiz[i])
        score += val
        if outcomes[i] != -1:
            print(card["Hubert47"])
            print(str(actual_val) + ": " + str(outcomes[i]))
        i += 1
    print("Hubert: " + str(score/len(cards)))

    score = 0
    for card in cards:
        score += analyseHand(card["kermit"])[0]
    print("kermit: " + str(score/len(cards)))

    score = 0
    for card in cards:
        score += analyseHand(card["kermit:2"])[0]
    print("kermit2: " + str(score/len(cards)))

    print('Ende')
