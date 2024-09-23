import copy
from bidding.bidder import Bidder
from iss.SkatMatch import SkatMatch
from skatzero.evaluation.utils import swap_colors
from skatzero.game.utils import get_points, init_32_deck
from iss_api import prepare_env, parse_bid, prepare_state_for_cardplay
from skatzero.test.utils import available_actions


def declare(args, gamemode):
    _, env, raw_state = prepare_env()

    raw_state['current_hand'] = [card for card in args[1].split(',')]
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
    bids, bid_jacks = parse_bid(int(args[3]), 1, bids, bid_jacks)
    bids, bid_jacks = parse_bid(int(args[4]), 2, bids, bid_jacks)
    raw_state['bids'] = bids
    raw_state['bid_jacks'] = bid_jacks
    raw_state['blind_hand'] = False

    bidder = Bidder(env, raw_state, args[2])

    game_discards, x = bidder.find_best_game_and_discard(bidder.raw_state)

    gametype_values = {}
    current_state = copy.deepcopy(raw_state)
    for gametype in ['C', 'S', 'H', 'D', 'G', 'N', 'NO']:
        bid_values = bidder.simulated_data_bidder.get_bid_value_table(current_state, gametype, bidder.estimates[gametype], penalty=False)
        bid_values = dict(zip(bidder.simulated_data_bidder.bids, bid_values))
        gametype_values[gametype] = bid_values[int(args[5])]

    # print(gametype_values[gamemode])
    return gametype_values[gamemode], game_discards

def cardplay(args):
    agents, env, raw_state = prepare_env()

    raw_state = prepare_state_for_cardplay(raw_state, env, args)

    state = env.extract_state(raw_state)

    agent_mode = 0
    if args[1] == 'G':
        agent_mode = 3
    if args[1] == 'N':
        agent_mode = 6

    _, info = agents[agent_mode + raw_state['self']].eval_step(state, True)

    card_to_play = max(info['values'], key=info['values'].get)
    max_value = info['values'][card_to_play]
    if args[1] in ['H', 'S', 'C']:
        card_to_play = swap_colors([card_to_play], 'D', args[1])[0]

    for k, v in info['values'].items():
        info['values'][k] = round(v, 2)
    sorted_dict = sorted(info['values'].items(), key=lambda x: -x[1])
    # for tpl in sorted_dict:
    #     if args[1] in ['H', 'S', 'C']:
    #         print(swap_colors([tpl[0]], 'D', args[1])[0], tpl[1])
    #     else:
    #         print(tpl[0], tpl[1])

    #print(card_to_play)
    #print(max_value)
    return max_value

if __name__ == '__main__':

    gametype = 'N'

    diff = 0
    diff2 = 0
    diff3 = 0
    diff4 = 0

    with open('C:/Users/janvo/Desktop/Skat/skatgame-games-07-2024/high_elo_' + gametype + '.txt', encoding='utf-8') as fRaw:

        line = fRaw.readline()

        i = 0

        while line:
            try:
                match = SkatMatch(line)
                if not match.eingepasst and (gametype == match.gameType or (gametype == 'D' and match.gameType[0] in ['H', 'S', 'C'])):
                    if match.alleinspielerInd == 1 and match.skatTaken and len(match.history) > 3:
                        args = [None, None, None, None, None, None]
                        args[0] = "DISCARD_AND_DECL"
                        args[1] = ','.join(match.cards[match.playerNames[match.alleinspielerInd]] + match.originalSkat)
                        args[2] = match.alleinspielerInd
                        args[3] = match.maxReizungen[(match.alleinspielerInd + 1) % 3]
                        args[4] = match.maxReizungen[(match.alleinspielerInd + 2) % 3]
                        args[5] = max(match.maxReizungen[(match.alleinspielerInd + 1) % 3], match.maxReizungen[(match.alleinspielerInd + 2) % 3], 18)
                        #print(args)
                        value, discards = declare(args, match.gameType[0])
                        args[2] = 0
                        value2, discards2 = declare(args, match.gameType[0])
                        discards = discards[match.gameType[0]]
                        #print(discards)
                        if discards[0] not in match.gedrueckt_cards or discards[1] not in match.gedrueckt_cards:
                            line = fRaw.readline()
                            continue

                        args = [None, None, None, None, None, None, None, None, None, None, None, None, None]
                        args[0] = "CARDPLAY"
                        args[1] = match.gameType[0]
                        args[2] = ','.join( [a for a in match.cards[match.playerNames[match.alleinspielerInd]] + match.originalSkat if a not in match.gedrueckt_cards])
                        args[3] = get_points(match.gedrueckt_cards[0]) + get_points(match.gedrueckt_cards[1])
                        args[4] = 0
                        args[5] = match.maxReizungen[(match.alleinspielerInd + 1) % 3]
                        args[6] = match.maxReizungen[(match.alleinspielerInd + 2) % 3]
                        args[7] = match.gedrueckt_cards[0]
                        args[8] = match.gedrueckt_cards[1]
                        args[9] = 0
                        args[10] = 0
                        args[11] = "??"
                        if match.alleinspielerInd == 1:
                            args[12] = "2" + match.history[1]
                        else:
                            args[12] = "1" + match.history[1] + ",2" + match.history[3]

                        #print(args)

                        correct_value = cardplay(args)

                        print(value)
                        print(correct_value)
                        print(abs(value - correct_value))

                        diff += abs(value - correct_value)
                        diff2 += abs(value2 - correct_value)
                        diff3 += value - correct_value
                        diff4 += value2 - correct_value

                        if i > 100:
                            break
                        i += 1
                        print(i)

                        print("##############")
            except:
                pass
            line = fRaw.readline()
        print(diff/100)
        print(diff2/100)
        print(diff3/100)
        print(diff4/100)
