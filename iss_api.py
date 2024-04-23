import sys
import os
from bidding.bidder import Bidder
from bidding.bidder_advanced import AdvancedBidder
from skatzero.env.skat import SkatEnv
from skatzero.evaluation.simulation import load_model
from skatzero.evaluation.utils import swap_bids, swap_colors
from skatzero.game.utils import calculate_bidding_value, init_32_deck
from skatzero.test.utils import available_actions, construct_state_from_history

def parse_history(history, trump): # Parsing history in the form of "1HT,2HA,0H8,..."
    cards = []
    for triplet in history.split(','):
        if trump in ['H', 'S', 'C']:
            card = swap_colors([triplet[1] + triplet[2]], 'D', trump)[0]
        else:
            card = triplet[1] + triplet[2]
        cards.append((int(triplet[0]), card))
    return cards

def parse_bid(bid, pos, bids, bid_jacks):
    d_bids = [18, 27, 45]
    h_bids = [20, 30, 40, 50]
    s_bids = [22, 33, 44, 55]
    c_bids = [24, 36, 48, 60]
    n_bids = [23, 35, 46, 59]

    if bid in d_bids:
        bids[pos]['D'] = 1
        if bid != 18:
            bid_jacks[pos] = int(bid / 9) - 1
    elif bid in h_bids:
        bids[pos]['H'] = 1
        bid_jacks[pos] = int(bid / 10) - 1
    elif bid in s_bids:
        bids[pos]['S'] = 1
        bid_jacks[pos] = int(bid / 11) - 1
    elif bid in c_bids:
        bids[pos]['C'] = 1
        bid_jacks[pos] = int(bid / 12) - 1
    elif bid in n_bids:
        bids[pos]['N'] = 1

    return bids, bid_jacks

def calculate_bids_for_gametypes(raw_state, estimates, bid_threshold, raw_bids):
    bid_list = []
    multiplier = calculate_bidding_value(raw_state['current_hand'])
    for i, val in enumerate(estimates):
        if val <= bid_threshold and not raw_bids:
            bid_list.append(0)
            continue
        if val <= 25 + bid_threshold and not raw_bids and not (i in [5, 6, 12, 13]): # 25 is average loss of value when others bid. Not valid for Null Games. #TODO: Check actual loss in Nullgames
            bid_list.append(18)
            continue
        if val <= 40 + bid_threshold and not raw_bids and i in [4, 11]: # Grand
            bid_list.append(18)
            continue
        if val <= 60 + bid_threshold and not raw_bids and i in [4, 11]: # Grand
            bid_list.append(24)
            continue
        hand = 0
        base_value = 24
        if i < 7:
            hand = 1
        if (i % 7) == 0:
            base_value = 12
        if (i % 7) == 1:
            base_value = 11
        if (i % 7) == 2:
            base_value = 10
        if (i % 7) == 3:
            base_value = 9
        bid = (multiplier + hand) * base_value
        if i == 12: # N
            bid = 23
        if i == 5: # NH
            bid = 35
        if i == 13: # NO
            bid = 46
        if i == 6: # NOH
            bid = 59
        bid_list.append(bid)
    return bid_list

def prepare_env():
    basedir = os.path.dirname(os.path.realpath(__file__))

    agents = []

    for gametype in ['D', 'G', 'N']:
        for i in range(0, 3):
            agents.append(load_model(basedir + "/models/latest/" + gametype + "_" + str(i) + ".pth"))

    env = SkatEnv(blind_hand_chance=0, open_hand_chance=0)

    env.set_agents(agents)

    raw_state, _ = env.game.init_game(blind_hand=True, open_hand=False)

    return agents, env, raw_state

def prepare_state_for_cardplay(raw_state, env, args):
    raw_state['current_hand'] = [card for card in args[2].split(',')]
    raw_state['self'] = int(args[10])
    raw_state['points'] = [int(args[3]), int(args[4])]

    bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    bid_jacks = [0, 0, 0]
    if args[10] != '1':
        bids, bid_jacks = parse_bid(int(args[5]), 1, bids, bid_jacks)
    if args[10] != '2':
        bids, bid_jacks = parse_bid(int(args[6]), 2, bids, bid_jacks)
    if args[7] != "??" and args[8] != "??":
        raw_state['skat'] = [args[7], args[8]]
    else:
        raw_state['skat'] = []
    raw_state['blind_hand'] = bool(int(args[9]))

    if args[1] in ['H', 'S', 'C']:
        raw_state['current_hand'] = swap_colors(raw_state['current_hand'], 'D', args[1])
        raw_state['skat'] = swap_colors(raw_state['skat'], 'D', args[1])
        raw_state['trace'] = swap_colors(raw_state['trace'], 'D', args[1])
        bids[1] = swap_bids(bids[1], 'D', args[1])
        bids[2] = swap_bids(bids[2], 'D', args[1])
    if args[1] == 'N':
        raw_state['trump'] = None
        env.game.round.trump = None
        env.game.gametype = 'N'
        env.game.round.gametype = 'N'
    if args[1] == 'G':
        raw_state['trump'] = 'J'
        env.game.round.trump = 'J'
        env.game.gametype = 'G'
        env.game.round.gametype = 'G'
    raw_state['bids'] = bids
    raw_state['bid_jacks'] = bid_jacks

    raw_state['soloplayer_open_cards'] = []
    raw_state['open_hand'] = False
    if args[11] != '??':
        raw_state['soloplayer_open_cards'] = args[11].split(',')
        raw_state['open_hand'] = True

    raw_state['trace'] = []
    if len(args) > 12 and args[12] is not None and args[12] != "":
        raw_state['trace'] = parse_history(args[12], args[1])

    if args[1] == 'N':
        played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'], trump = None)
    elif args[1] == 'G':
        played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'], trump = 'J')
    else:
        played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'], trump = 'D')

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick

    return raw_state

def bid(args, accuracy, bid_threshold):
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

    if args[0] == 'SKAT_OR_HAND_DECL':
        bids, bid_jacks = parse_bid(int(args[3]), 1, bids, bid_jacks)
        bids, bid_jacks = parse_bid(int(args[4]), 2, bids, bid_jacks)

    raw_state['bids'] = bids
    raw_state['bid_jacks'] = bid_jacks

    bidder = AdvancedBidder(env, raw_state, args[2])
    hand_estimates = bidder.get_blind_hand_values()
    for _ in range(accuracy):
        mean_estimates, bid_value_dict = bidder.update_value_estimates()
    pickup_estimates = [sum(mean_estimates['C']) / len(mean_estimates['C']),
                        sum(mean_estimates['S']) / len(mean_estimates['S']),
                        sum(mean_estimates['H']) / len(mean_estimates['H']),
                        sum(mean_estimates['D']) / len(mean_estimates['D']),
                        sum(mean_estimates['G']) / len(mean_estimates['G']),
                        sum(mean_estimates['N']) / len(mean_estimates['N']),
                        sum(mean_estimates['NO']) / len(mean_estimates['NO'])]

    all_estimates = pickup_estimates + hand_estimates
    for k, v in enumerate(all_estimates):
        all_estimates[k] = round(v, 2)
    for i, gametype in enumerate(['C ', 'S ', 'H ', 'D ', 'G', 'N', 'NO', 'CH', 'SH', 'HH', 'DH', 'GH', 'NH', 'NOH']):
        print(gametype, all_estimates[i])

    if args[0] == 'SKAT_OR_HAND_DECL':
        bid_list = calculate_bids_for_gametypes(raw_state, hand_estimates + pickup_estimates, bid_threshold, True)
        for i, _ in enumerate(hand_estimates): # Set hand games that are not possible with the bid to -1000. #TODO: Remove when hand value table is implemented
            if bid_list[i] < int(args[5]):
                hand_estimates[i] = -1000

        pickup_average_estimate = bid_value_dict[int(args[5])]

        if pickup_average_estimate > max(hand_estimates):
            print('s')
            return
        else:
            gametype = hand_estimates.index(max(hand_estimates))
            str_type = 'NO'
            if gametype == 0:
                str_type = 'C'
            if gametype == 1:
                str_type = 'S'
            if gametype == 2:
                str_type = 'H'
            if gametype == 3:
                str_type = 'D'
            if gametype == 4:
                str_type = 'G'
            if gametype == 5:
                str_type = 'N'

            if str_type == 'NO':
                declaration = 'NHO'
                for card in raw_state['current_hand']:
                    declaration = declaration + "." + card
                print(declaration)
            else:
                print(str_type + 'H')
            return
    elif args[0] == 'BID':
        bid_list_hand = calculate_bids_for_gametypes(raw_state, hand_estimates, bid_threshold, False)
        highest_bid_hand = max(bid_list_hand)

        max_bid = 0
        if bid_value_dict[18] > 0:
            max_bid = 18
        try:
            max_bid = [key for key, value in bid_value_dict.items() if value > 25][-1]
        except:
            pass
        highest_bid = max(highest_bid_hand, max_bid)

        print(str(highest_bid))
        return

def declare(args):
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

    game_discards = bidder.find_best_game_and_discard(bidder.raw_state)

    multiplier = calculate_bidding_value(raw_state['current_hand'])

    best = -999
    for key, value in bidder.estimates.items():
        base_value = 9
        if key == 'G':
            base_value = 24
        if key == 'C':
            base_value = 12
        elif key == 'S':
            base_value = 11
        elif key == 'H':
            base_value = 10
        elif key == 'D':
            base_value = 9
        bid = multiplier * base_value
        if key == 'N':
            bid = 23
        if key == 'NH':
            bid = 35
        if key == 'NO':
            bid = 46
        if key == 'NOH':
            bid = 59
        if bid < int(args[5]):
            continue
        if value[0] > best:
            best = value[0]

    if best == -999: # Überreizt -> Spielt einfach das stärkste Spiel
        gametype = max(bidder.estimates, key=bidder.estimates.get)
    else:
        gametype = [k for k, v in bidder.estimates.items() if v == best][0]

    skat = game_discards[gametype]

    for k, v in bidder.estimates.items():
        bidder.estimates[k][0] = round(v[0], 2)
    sorted_dict = sorted(bidder.estimates.items(), key=lambda x: -x[1][0])
    for tpl in sorted_dict:
        print(tpl[0], tpl[1][0])

    if gametype == 'NO': # TODO: Müssen die Karten sortiert sein damit ISS damit umgehen kann?
        declaration = gametype + "." + skat[0] + "." + skat[1]
        for card in raw_state['current_hand']:
            if card != skat[0] and card != skat[1]:
                declaration = declaration + "." + card
        print(declaration)
    else:
        print(gametype + "." + skat[0] + "." + skat[1])


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
    if args[1] in ['H', 'S', 'C']:
        card_to_play = swap_colors([card_to_play], 'D', args[1])[0]

    for k, v in info['values'].items():
        info['values'][k] = round(v, 2)
    sorted_dict = sorted(info['values'].items(), key=lambda x: -x[1])
    for tpl in sorted_dict:
        if args[1] in ['H', 'S', 'C']:
            print(swap_colors([tpl[0]], 'D', args[1])[0], tpl[1])
        else:
            print(tpl[0], tpl[1])

    print(card_to_play)


if __name__ == '__main__':
    ACCURACY = 50 # Number of Iterations for Skat simulation
    BID_THRESHOLD = 0 # How aggressive should the AI bid? 0 is average best return, lower values mean more aggressive

    args = sys.argv[1:]

    if args[0] == 'BID':
        bid(args, ACCURACY, BID_THRESHOLD)
    elif args[0] == 'SKAT_OR_HAND_DECL':
        bid(args, ACCURACY, BID_THRESHOLD)
    elif args[0] == 'DISCARD_AND_DECL':
        declare(args)
    elif args[0] == 'CARDPLAY':
        if args[1] in ['D', 'H', 'S', 'C', 'G', 'N']:
            cardplay(args)
        else:
            print("Wrong Gamemode")
