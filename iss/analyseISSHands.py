from bidding.bidder_advanced import AdvancedBidder
from iss.SkatMatch import SkatMatch
from iss_api import prepare_env
from skatzero.game.utils import init_32_deck
from skatzero.test.utils import available_actions


def getHandsFromLogFile(logFilePath):
    cards = []
    print('Reading file...')
    with open(logFilePath) as fRaw:

        line = fRaw.readline()

        while line:
            try:
                match = SkatMatch(line)
                cards.append(match.cards)
            except:
                pass
            line = fRaw.readline()
    return cards

def analyseHand(cards):
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

    bidder = AdvancedBidder(env, raw_state, 0, penalties)
    hand_estimates = bidder.get_blind_hand_values()

    return max(hand_estimates)

if __name__ == '__main__':
    # Parameter
    issLogFilePath = 'C:/Users/janvo/Desktop/Skat/ISS-Bot/log.txt'

    cards = getHandsFromLogFile(issLogFilePath)

    score = 0
    for card in cards:
        score += analyseHand(card["Hubert47"])
    print("Hubert: " + str(score/len(cards)))

    score = 0
    for card in cards:
        score += analyseHand(card["zoot"])
    print("Zoot: " + str(score/len(cards)))

    score = 0
    for card in cards:
        score += analyseHand(card["zoot:2"])
    print("Zoot2: " + str(score/len(cards)))

    print('Ende')
