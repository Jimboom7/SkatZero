import sys
import os
from skatzero.env.skat import SkatEnv
from skatzero.evaluation.bidder import Bidder
from skatzero.evaluation.simulation import load_model
from skatzero.evaluation.utils import swap_colors
from skatzero.game.utils import calculate_bidding_value, init_32_deck
from skatzero.test.utils import available_actions, construct_state_from_history

def parse_history(history, trump): # Parsing history in the form of "1HT,2HA,0H8,..."
    cards = []
    for triplet in history.split(','):
        card = swap_colors([triplet[1] + triplet[2]], 'D', trump)[0]
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

def calculate_bids_for_gametypes(raw_state, estimates, raw_bids=False):
    bid_list = []
    multiplier = calculate_bidding_value(raw_state['current_hand'])
    for i, val in enumerate(estimates): # TODO: Startposition einrechnen
        if val <= 0 and not raw_bids:
            bid_list.append(0)
            continue
        if val <= 10 and not raw_bids:
            bid_list.append(18)
            continue
        hand = 0
        base_value = 9
        if i < 4:
            hand = 1
        if (i % 4) == 0:
            base_value = 12
        if (i % 4) == 1:
            base_value = 11
        if (i % 4) == 2:
            base_value = 10
        bid = (multiplier + hand) * base_value
        bid_list.append(bid)
    return bid_list

def prepare_env(model, version):
    BASEDIR = os.path.dirname(os.path.realpath(__file__))

    MODEL1 = BASEDIR + "/checkpoints/" + model + "/0_" + str(version) + ".pth"
    MODEL2 = BASEDIR + "/checkpoints/" + model + "/1_" + str(version) + ".pth"
    MODEL3 = BASEDIR + "/checkpoints/" + model + "/2_" + str(version) + ".pth"

    models = [
            MODEL1,
            MODEL2,
            MODEL3
        ]

    agents = []
    for _, model_path in enumerate(models):
        agents.append(load_model(model_path))

    env = SkatEnv()

    env.set_agents(agents)

    raw_state, _ = env.game.init_game(blind_hand=True)

    return agents, env, raw_state

def prepare_state_for_cardplay(raw_state, args):
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
    raw_state['hand'] = bool(args[9])

    raw_state['current_hand'] = swap_colors(raw_state['current_hand'], 'D', args[1])
    raw_state['skat'] = swap_colors(raw_state['skat'], 'D', args[1])
    raw_state['trace'] = swap_colors(raw_state['trace'], 'D', args[1])
    tmp = bids[1]['D']
    bids[1]['D'] = bids[1][args[1]]
    bids[1][args[1]] = tmp
    tmp = bids[2]['D']
    bids[2]['D'] = bids[2][args[1]]
    bids[2][args[1]] = tmp
    raw_state['bids'] = bids
    raw_state['bid_jacks'] = bid_jacks

    raw_state['trace'] = []
    if len(args) > 11 and args[11] is not None and args[11] != "":
        raw_state['trace'] = parse_history(args[11], args[1])

    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick

    return raw_state

def bid(model, version, args):
    _, env, raw_state = prepare_env(model, version)

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
        bids, bid_jacks = parse_bid(int(args[2]), 1, bids, bid_jacks)
        bids, bid_jacks = parse_bid(int(args[3]), 2, bids, bid_jacks)

    raw_state['bids'] = bids
    raw_state['bid_jacks'] = bid_jacks

    bidder = Bidder(env, raw_state)
    hand_estimates = bidder.get_blind_hand_values()
    for _ in range(50):
        mean_estimates = bidder.update_value_estimates()
    pickup_estimates = [sum(mean_estimates['C']) / len(mean_estimates['C']),
                        sum(mean_estimates['S']) / len(mean_estimates['S']),
                        sum(mean_estimates['H']) / len(mean_estimates['H']),
                        sum(mean_estimates['D']) / len(mean_estimates['D'])]

    all_estimates = pickup_estimates + hand_estimates
    for k, v in enumerate(all_estimates):
        all_estimates[k] = round(v, 2)
    for i, gametype in enumerate(['C ', 'S ', 'H ', 'D ', 'CH', 'SH', 'HH', 'DH']):
        print(gametype, all_estimates[i])

    if args[0] == 'SKAT_OR_HAND_DECL':
        bid_list = calculate_bids_for_gametypes(raw_state, hand_estimates + pickup_estimates, raw_bids=True)
        for i, _ in enumerate(pickup_estimates): # TODO: Kreuz etc. Value mit einrechnen?
            if bid_list[i + 4] < int(args[4]):
                pickup_estimates[i] = -100
        for i, _ in enumerate(hand_estimates):
            if bid_list[i] < int(args[4]):
                hand_estimates[i] = -100
        if max(pickup_estimates) > max(hand_estimates):
            print('s')
            return
        else:
            gametype = hand_estimates.index(max(hand_estimates))
            str_type = 'D'
            if gametype == 0:
                str_type = 'C'
            if gametype == 1:
                str_type = 'S'
            if gametype == 2:
                str_type = 'H'
            print(str_type + 'H')
            return
    elif args[0] == 'BID':
        bid_list = calculate_bids_for_gametypes(raw_state, hand_estimates + pickup_estimates)
        highest_bid = max(bid_list)
        print(str(highest_bid))
        return

def declare(model, version, args):
    _, env, raw_state = prepare_env(model, version)

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
    bids, bid_jacks = parse_bid(int(args[2]), 1, bids, bid_jacks)
    bids, bid_jacks = parse_bid(int(args[3]), 2, bids, bid_jacks)
    raw_state['bids'] = bids
    raw_state['bid_jacks'] = bid_jacks
    raw_state['blind_hand'] = False

    bidder = Bidder(env, raw_state)

    game_discards = bidder.find_best_game_and_discard(raw_state)

    multiplier = calculate_bidding_value(raw_state['current_hand'])

    best = -999
    for key, value in bidder.estimates.items():
        base_value = 9
        if key == 'C':
            base_value = 12
        elif key == 'S':
            base_value = 11
        elif key == 'H':
            base_value = 10
        elif key == 'D':
            base_value = 9
        if multiplier * base_value < int(args[4]):
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

    print(gametype + "." + skat[0] + "." + skat[1])


def cardplay(model, version, args):
    agents, env, raw_state = prepare_env(model, version)

    raw_state = prepare_state_for_cardplay(raw_state, args)

    state = env.extract_state(raw_state)

    _, info = agents[raw_state['self']].eval_step(state)

    card_to_play = max(info['values'], key=info['values'].get)
    card_to_play = swap_colors([card_to_play], 'D', args[1])[0]

    for k, v in info['values'].items():
        info['values'][k] = round(v, 2)
    sorted_dict = sorted(info['values'].items(), key=lambda x: -x[1])
    for tpl in sorted_dict:
        print(swap_colors([tpl[0]], 'D', args[1])[0], tpl[1])

    print(card_to_play)


if __name__ == '__main__':
    MODEL = "skat_30_final"
    FRAMES = 5690

    args = sys.argv[1:]

    if args[0] == 'BID':
        bid(MODEL, FRAMES, args)
    elif args[0] == 'SKAT_OR_HAND_DECL':
        bid(MODEL, FRAMES, args)
    elif args[0] == 'DISCARD_AND_DECL':
        declare(MODEL, FRAMES, args)
    elif args[0] == 'CARDPLAY':
        if args[1] in ['D', 'H', 'S', 'C']:
            cardplay(MODEL, FRAMES, args)
        else:
            print("Wrong Gamemode")
