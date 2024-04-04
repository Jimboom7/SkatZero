import sys
import os
from skatzero.env.feature_transformations import convert_card_to_action_id
from skatzero.env.skat import SkatEnv
from skatzero.evaluation.simulation import load_model
from skatzero.evaluation.utils import swap_colors
from skatzero.test.utils import construct_state_from_history

def parse_history(history, trump): # Parsing history in the form of "1HT,2HA,0H8"
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

def run(model, version, args):
    if not args[9] in ['D', 'H', 'S', 'C']:
        print("Wrong Gamemode")

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

    raw_state, _ = env.game.init_game(blind_hand=False)

    raw_state['self'] = int(args[0])
    raw_state['current_hand'] = [card for card in args[1].split(',')]
    raw_state['points'] = [int(args[2]), int(args[3])]

    bids = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    bid_jacks = [0, 0, 0]
    if args[0] != '1':
        bids, bid_jacks = parse_bid(int(args[4]), 1, bids, bid_jacks)
    if args[0] != '2':
        bids, bid_jacks = parse_bid(int(args[5]), 2, bids, bid_jacks)
    raw_state['bids'] = bids
    raw_state['bid_jacks'] = bid_jacks
    if args[6] != "??" and args[7] != "??":
        raw_state['skat'] = [args[6], args[7]]
    else:
        raw_state['skat'] = []
    raw_state['hand'] = bool(args[8])

    raw_state['current_hand'] = swap_colors(raw_state['current_hand'], 'D', args[9])
    raw_state['skat'] = swap_colors(raw_state['skat'], 'D', args[9])
    raw_state['trace'] = swap_colors(raw_state['trace'], 'D', args[9])
    tmp = bids[1]['D']
    bids[1]['D'] = bids[1][args[9]]
    bids[1][args[9]] = tmp
    tmp = bids[2]['D']
    bids[2]['D'] = bids[2][args[9]]
    bids[2][args[9]] = tmp


    raw_state['trace'] = parse_history(args[10], args[9])

    played_cards, others_cards, trick, actions = construct_state_from_history(raw_state['current_hand'] , raw_state['trace'], raw_state['skat'])

    raw_state['played_cards'] = played_cards
    raw_state['others_hand'] = others_cards
    raw_state['actions'] = actions
    raw_state['trick'] = trick

    state = env.extract_state(raw_state)

    _, info = agents[raw_state['self']].eval_step(state)

    card_encoding = {'D': 0, 'H': 1, 'S': 2, 'C': 3}
    tmp = card_encoding['D']
    card_encoding['D'] = card_encoding[args[9]]
    card_encoding[args[9]] = tmp
    return_value = max(info['values'], key=info['values'].get)
    return_value = convert_card_to_action_id(return_value, card_encoding)

    # print(info)
    print(return_value)
    sys.exit(return_value)


if __name__ == '__main__':
    MODEL = "skat_30_final"
    FRAMES = 4750

    args = sys.argv[1:]

    run(MODEL, FRAMES, args)
