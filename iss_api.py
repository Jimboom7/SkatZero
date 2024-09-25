import copy
import sys
import os
import time

from bidding.bidder import Bidder
from skatzero.env.skat import SkatEnv
from skatzero.evaluation.simulation import load_model
from skatzero.evaluation.utils import swap_bids, swap_colors
from skatzero.game.utils import compare_cards, get_points, init_32_deck
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

def prepare_env():
    basedir = os.path.dirname(os.path.realpath(__file__))

    agents = []

    for gametype in ['D', 'G', 'N']:
        for i in range(0, 3):
            agents.append(load_model(basedir + "/models/latest/" + gametype + "_" + str(i) + ".pth"))
    # for i in range(0, 3):
    #     agents.append(load_model(basedir + "/models/checkpoints/skat_lstm_D/" + str(i) + "_17000.pth"))
    # for i in range(0, 3):
    #     agents.append(load_model(basedir + "/models/checkpoints/skat_lstm_G/" + str(i) + "_14140.pth"))
    # for i in range(0, 3):
    #     agents.append(load_model(basedir + "/models/checkpoints/skat_lstm_N/" + str(i) + "_3800.pth"))

    env = SkatEnv()

    env.set_agents(agents)

    raw_state, _ = env.game.init_game()
    env.game.round.blind_hand = True
    env.game.round.open_hand = False
    raw_state['blind_hand'] = True
    raw_state['open_hand'] = False
    raw_state['points'] = [0, 0]
    raw_state['drueck'] = False

    return agents, env, raw_state

def prepare_state_for_cardplay(raw_state, env, args):
    raw_state['current_hand'] = [card for card in args[2].split(',')]
    raw_state['self'] = int(args[11])
    raw_state['points'] = [int(args[4]), int(args[5])]
    raw_state['pos'] = (3 - int(args[3])) % 3

    bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    bid_jacks = [0, 0, 0]
    if args[11] != '1':
        bids, bid_jacks = parse_bid(int(args[6]), 1, bids, bid_jacks)
    if args[11] != '2':
        bids, bid_jacks = parse_bid(int(args[7]), 2, bids, bid_jacks)
    if args[8] != "??" and args[9] != "??":
        raw_state['skat'] = [args[8], args[9]]
    else:
        raw_state['skat'] = []
    raw_state['blind_hand'] = bool(int(args[10]))

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
    if args[12] != '??':
        raw_state['soloplayer_open_cards'] = args[12].split(',')
        raw_state['open_hand'] = True

    raw_state['trace'] = []
    if len(args) > 13 and args[13] is not None and args[13] != "":
        raw_state['trace'] = parse_history(args[13], args[1])

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
    raw_state['pos'] = (3 - int(args[2])) % 3

    hand_bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    bid_jacks = [0, 0, 0]
    penalties = {'D': 15, 'G': 40, 'N': 0, 'NO': 0, 'DH': 30, 'GH': 60, 'NH': 0, 'NOH': 0}

    if args[0] == 'SKAT_OR_HAND_DECL':
        hand_bids, bid_jacks = parse_bid(int(args[3]), 1, hand_bids, bid_jacks)
        hand_bids, bid_jacks = parse_bid(int(args[4]), 2, hand_bids, bid_jacks)
        penalties = {'D': 0, 'G': 0, 'N': 0, 'NO': 0, 'DH': 0, 'GH': 0, 'NH': 0, 'NOH': 0}

    raw_state['bids'] = hand_bids
    raw_state['bid_jacks'] = bid_jacks

    bidder = Bidder(env, raw_state, args[2], penalties)
    hand_estimates = bidder.get_blind_hand_values()
    start_time = time.time()
    for _ in range(accuracy):
        mean_estimates, bid_value_dict = bidder.update_value_estimates()
        if time.time() - start_time > 60: # Stop after 1 min max or 100 iterations
            break
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
        bid_hand_dict = bidder.get_blind_hand_bidding_table(hand_estimates, return_only_max=False, penalty=False)

        hand_bids = []
        for i, gametype in enumerate(['CH', 'SH', 'HH', 'DH', 'GH', 'NH', 'NOH']):
            hand_bids.append(bid_hand_dict[gametype][int(args[5])])

        pickup_average_estimate = bid_value_dict[int(args[5])]

        print(pickup_average_estimate)
        print(hand_bids)

        if pickup_average_estimate > max(hand_bids):
            print('s')
            return
        else:
            gametype = hand_bids.index(max(hand_bids))
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
        bid_hand_dict = bidder.get_blind_hand_bidding_table(hand_estimates, return_only_max=True, penalty=True)

        max_bid_hand = get_max_bid(bid_threshold, bid_hand_dict)

        max_bid = get_max_bid(bid_threshold, bid_value_dict)

        highest_bid = max(max_bid_hand, max_bid)

        print(bid_hand_dict)
        print(bid_value_dict) # TODO: Remove? Pretty Print?

        print(str(highest_bid))
        return

def get_max_bid(bid_threshold, bid_dict):
    max_bid_hand = 0
    if bid_dict[18] > -5 + bid_threshold:
        max_bid_hand = 17
    try:
        max_bid_hand = [key for key, value in bid_dict.items() if value > bid_threshold + 10 or (value > bid_threshold and int(key) < 27)][-1]
    except IndexError:
        pass
    return max_bid_hand

def declare(args):
    _, env, raw_state = prepare_env()

    raw_state['current_hand'] = [card for card in args[1].split(',')]
    others_cards = init_32_deck()
    for c in raw_state['current_hand']:
        others_cards.remove(c)
    raw_state['others_hand'] = others_cards
    raw_state['skat'] = []
    raw_state['actions'] = available_actions(raw_state['current_hand'])
    raw_state['pos'] = (3 - int(args[2])) % 3

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

    game_discards, _ = bidder.find_best_game_and_discard(bidder.raw_state)

    current_state = copy.deepcopy(raw_state)
    gametype_values = {}
    for gametype in ['C', 'S', 'H', 'D', 'G', 'N', 'NO']:
        bid_values = bidder.simulated_data_bidder.get_bid_value_table(current_state, gametype, bidder.estimates[gametype], penalty=False)
        bid_values = dict(zip(bidder.simulated_data_bidder.bids, bid_values))
        gametype_values[gametype] = bid_values[int(args[5])]

    best_gametype = max(gametype_values, key=gametype_values.get)

    skat = game_discards[best_gametype]

    for k, v in gametype_values.items():
        gametype_values[k] = round(v, 2)
    sorted_dict = sorted(gametype_values.items(), key=lambda x: -x[1])
    for tpl in sorted_dict:
        print(tpl[0], tpl[1])

    if best_gametype == 'NO':
        declaration = best_gametype + "." + skat[0] + "." + skat[1]
        for card in raw_state['current_hand']:
            if card != skat[0] and card != skat[1]:
                declaration = declaration + "." + card
        print(declaration)
    else:
        print(best_gametype + "." + skat[0] + "." + skat[1])

def cardplay(args, recursed=False):
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
    for tpl in sorted_dict:
        if args[1] in ['H', 'S', 'C']:
            if not recursed:
                print(swap_colors([tpl[0]], 'D', args[1])[0], tpl[1])
        else:
            if not recursed:
                print(tpl[0], tpl[1])

    if not recursed:
        print(card_to_play)
    if recursed:
        return max_value
    if len(raw_state["current_hand"]) > 1 and len(raw_state["trick"]) == 2 and args[1] != 'N': # full trick: check if self is next, then calculate next state and best discard value for each card
        card_values = {}
        for card_swapped in raw_state['actions']:
            if args[1] in ['H', 'S', 'C']:
                card = swap_colors([card_swapped], 'D', args[1])[0]
            else:
                card = card_swapped
            current_state = copy.deepcopy(raw_state)
            current_state['trick'].append((0, card_swapped))
            winner, points = check_trick(current_state['trick'], raw_state['trump'])
            if winner != 2:
                if args[1] in ['H', 'S', 'C']:
                    card_values[card_swapped] = info['values'][card_swapped]
                else:
                    card_values[card_swapped] = info['values'][card_swapped]
            else:
                args_for_next_turn = args.copy()
                args_for_next_turn[13] += ',' + str(raw_state["self"]) + card
                args_for_next_turn[2] = args_for_next_turn[2].replace(card, '').replace(',,', ',').strip(',')
                if raw_state["self"] == 0:
                    args_for_next_turn[4] = int(args_for_next_turn[4]) + points
                else:
                    args_for_next_turn[5] = int(args_for_next_turn[5]) + points
                card_values[card_swapped] = cardplay(args_for_next_turn, True)
        print("After recursion:")
        for k, v in card_values.items():
            card_values[k] = round(v, 2)
        sorted_dict = sorted(card_values.items(), key=lambda x: -x[1])
        for tpl in sorted_dict:
            if args[1] in ['H', 'S', 'C']:
                if not recursed:
                    print(swap_colors([tpl[0]], 'D', args[1])[0], tpl[1])
            else:
                if not recursed:
                    print(tpl[0], tpl[1])
        card_to_play = max(card_values, key=card_values.get)
        if args[1] in ['H', 'S', 'C']:
            card_to_play = swap_colors([card_to_play], 'D', args[1])[0]
        print(card_to_play)

def check_trick(trick, trump):
    winner = 0
    card1 = trick[0][1]
    card2 = trick[1][1]
    card3 = trick[2][1]
    highest_card = card1
    if not compare_cards(card1, card2, trump, card1[0]):
        highest_card = card2
        winner = 1
    if not compare_cards(highest_card, card3, trump, card1[0]):
        winner = 2
    points = get_points(card1) + get_points(card2) + get_points(card3)
    return winner, points

if __name__ == '__main__':
    ACCURACY = 231 # Number of Iterations for Skat simulation
    BID_THRESHOLD = -5 # How aggressive should the AI bid? 0 is average best return if the opponents never play themselves, -20 is average considering opponent solo games

    arguments = sys.argv[1:]

    if arguments[0] == 'BID':
        bid(arguments, ACCURACY, BID_THRESHOLD)
    elif arguments[0] == 'SKAT_OR_HAND_DECL':
        bid(arguments, ACCURACY, BID_THRESHOLD)
    elif arguments[0] == 'DISCARD_AND_DECL':
        declare(arguments)
    elif arguments[0] == 'CARDPLAY':
        if arguments[1] in ['D', 'H', 'S', 'C', 'G', 'N']:
            cardplay(arguments)
        else:
            print("Wrong Gamemode")

    #DEBUG
    #declare(["DISCARD_AND_DECL", "CJ,DJ,DA,DK,DQ,D7,C9,HA,HT,HK,CT,ST", 0, 0, 0, 18])
