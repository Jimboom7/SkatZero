from collections import OrderedDict

import numpy as np

from skatzero.game.utils import card_rank_as_number, card_ranks

jack_encoding ={'C': 0, 'S': 1, 'H': 2, 'D': 3}

def convert_action_id_to_card(action_id, card_encoding):
    if action_id % 8 == 7: # Jack
        return list(jack_encoding.keys())[list(jack_encoding.values()).index(int(action_id / 8))] + card_ranks[action_id % 8]
    return list(card_encoding.keys())[list(card_encoding.values()).index(int(action_id / 8))] + card_ranks[action_id % 8]

def convert_card_to_action_id(action, card_encoding):
    if action[1] == 'J':
        return (jack_encoding[action[0]] * 8) + card_rank_as_number[action[1]]
    return (card_encoding[action[0]] * 8) + card_rank_as_number[action[1]]

def card2array(card, card_encoding):
    matrix = np.zeros([4, 8], dtype=np.int8)
    if card is None or card == '':
        return matrix.flatten()
    if card[1] == 'J':
        matrix[jack_encoding[card[0]], card_rank_as_number[card[1]]] = 1
    else:
        matrix[card_encoding[card[0]], card_rank_as_number[card[1]]] = 1
    return matrix.flatten()

def cards2array(cards, card_encoding):
    matrix = np.zeros([4, 8], dtype=np.int8)
    if cards is None or cards == ['']:
        return matrix.flatten()
    for card in cards:
        if card[1] == 'J':
            matrix[jack_encoding[card[0]], card_rank_as_number[card[1]]] = 1
        else:
            matrix[card_encoding[card[0]], card_rank_as_number[card[1]]] = 1
    return matrix.flatten()

def get_number_as_one_hot_vector(number, max_points=120):
    one_hot = np.zeros(max_points + 1, dtype=np.int8)
    one_hot[number] = 1
    return one_hot

def action_seq2array(action_seq_list, card_encoding):
    action_seq_array = np.zeros((len(action_seq_list), 32), np.int8)
    for row, card in enumerate(action_seq_list):
        action_seq_array[row, :] = card2array(card, card_encoding)
    action_seq_array = action_seq_array.flatten()
    return action_seq_array

def process_action_seq(sequence, length=30):
    sequence = [action[1] for action in sequence[-length:]]
    if len(sequence) % 3 == 1:
        sequence.append('')
        sequence.append('')
    if len(sequence) % 3 == 2:
        sequence.append('')
    if len(sequence) < length:
        empty_sequence = ['' for _ in range(length - len(sequence))]
        empty_sequence.extend(sequence)
        sequence = empty_sequence
    return sequence

def calculate_missing_cards(player_id, trace, trump, card_encoding):
    matrix = np.zeros([4, 8], dtype=np.int8)
    trick_counter = 0
    for player, card in trace:
        trick_counter += 1
        if player == player_id:
            player_card = card
        if trick_counter % 3 == 1:
            base_card = card
        if trick_counter % 3 == 0:
            if (player_card[0] == base_card[0]
                or ((player_card[1] == 'J' or player_card[0] == trump) and
                    (base_card[1] == 'J' or base_card[0] == trump))):
                continue
            if base_card[1] == 'J' or base_card[0] == trump:
                matrix[card_encoding[trump], :7] = 1
                matrix[:, 7] = 1
            else:
                matrix[card_encoding[base_card[0]], :7] = 1
    return matrix.flatten()

def get_card_encoding(state):
    encoding ={'D': 0, 'H': 1, 'S': 2, 'C': 3}
    num_h = len([d for d in state['current_hand'] if d[0] == 'H'])
    num_s = len([d for d in state['current_hand'] if d[0] == 'S'])
    num_c = len([d for d in state['current_hand'] if d[0] == 'C'])
    if max(num_h, num_s, num_c) == num_h:
        encoding = {'D': 0, 'H': 1, 'S': 2, 'C': 3}
        if max(num_s, num_c) == num_c:
            encoding = {'D': 0, 'H': 1, 'C': 2, 'S': 3}
    elif max(num_h, num_s, num_c) == num_s:
        encoding = {'D': 0, 'S': 1, 'H': 2, 'C': 3}
        if max(num_h, num_c) == num_c:
            encoding = {'D': 0, 'S': 1, 'C': 2, 'H': 3}
    elif max(num_h, num_s, num_c) == num_c:
        encoding = {'D': 0, 'C': 1, 'H': 2, 'S': 3}
        if max(num_h, num_s) == num_s:
            encoding = {'D': 0, 'C': 1, 'S': 2, 'H': 3}
    return encoding

def get_bid(bid_dict, card_encoding):
    matrix = np.zeros([5,], dtype=np.int8)
    for suit in ['D', 'H', 'S', 'C']:
        if bid_dict[suit] == 1:
            matrix[card_encoding[suit]] = 1
    if bid_dict['N'] == 1:
        matrix[4] = 1
    return matrix

def get_bid_jacks(bid_jacks):
    matrix = np.zeros([5,], dtype=np.int8)
    matrix[bid_jacks] = 1
    return matrix

def get_common_features(state):
    card_encoding = get_card_encoding(state)
    current_hand = cards2array(state['current_hand'], card_encoding)
    others_hand = cards2array(state['others_hand'], card_encoding)

    all_actions = action_seq2array(process_action_seq(state['trace']), card_encoding)

    trick1 = card2array(None, card_encoding)
    trick2 = card2array(None, card_encoding)
    if len(state['trick']) >= 1:
        trick1 = card2array(state['trick'][0][1], card_encoding)
    if len(state['trick']) == 2:
        trick2 = card2array(state['trick'][1][1], card_encoding)

    if state['blind_hand']:
        blind_hand = np.ones([1,], dtype=np.int8)
    else:
        blind_hand = np.zeros([1,], dtype=np.int8)

    return current_hand, others_hand, all_actions, trick1, trick2, blind_hand, card_encoding

def get_soloplayer_features(state):
    current_hand, others_hand, all_actions, trick1, trick2, blind_hand, card_encoding = get_common_features(state)

    opponent_left_played_cards = cards2array(state['played_cards'][2], card_encoding)
    opponent_right_played_cards = cards2array(state['played_cards'][1], card_encoding)

    missing_cards_left = calculate_missing_cards(2, state['trace'], state['trump'], card_encoding)
    missing_cards_right = calculate_missing_cards(1, state['trace'], state['trump'], card_encoding)

    points_own = get_number_as_one_hot_vector(state['points'][0])
    points_opp = get_number_as_one_hot_vector(state['points'][1])

    bid_left = get_bid(state['bids'][1], card_encoding)
    bid_right = get_bid(state['bids'][2], card_encoding)

    bid_jacks_left = get_bid_jacks(state['bid_jacks'][1])
    bid_jacks_right = get_bid_jacks(state['bid_jacks'][2])

    if not state['blind_hand']:
        skat = cards2array([state['skat'][0], state['skat'][1]], card_encoding)
    else:
        skat = cards2array(None, card_encoding)

    obs = np.concatenate((current_hand,  # 32
                            others_hand,  # 32
                            trick1,  # 32
                            trick2,  # 32
                            skat,  # 32
                            all_actions,  # 32*30
                            missing_cards_left,  # 32
                            opponent_left_played_cards,  # 32
                            missing_cards_right,  # 32
                            opponent_right_played_cards,  # 32
                            points_own,  # 121
                            points_opp, # 121
                            bid_left, # 5
                            bid_right, # 5
                            bid_jacks_left, # 5
                            bid_jacks_right, # 5
                            blind_hand)) # 1
    return obs

def get_opponent_features(state):
    current_hand, others_hand, all_actions, trick1, trick2, blind_hand, card_encoding = get_common_features(state)
    soloplayer_played_cards = cards2array(state['played_cards'][0], card_encoding)

    last_soloplayer_action = None
    for i, action in reversed(state['trace']):
        if i == state['soloplayer']:
            last_soloplayer_action = action
            break
    last_soloplayer_action = card2array(last_soloplayer_action, card_encoding)

    teammate_id = 3 - state['self']

    missing_cards_solo = calculate_missing_cards(0, state['trace'], state['trump'], card_encoding)
    missing_cards_teammate = calculate_missing_cards(teammate_id, state['trace'], state['trump'], card_encoding)

    points_own = get_number_as_one_hot_vector(state['points'][1])
    points_opp = get_number_as_one_hot_vector(state['points'][0])

    teammate_played_cards = cards2array(state['played_cards'][teammate_id], card_encoding)
    last_teammate_action = None
    for i, action in reversed(state['trace']):
        if i == teammate_id:
            last_teammate_action = action
            break
    last_teammate_action = card2array(last_teammate_action, card_encoding)

    bid_teammate = get_bid(state['bids'][teammate_id], card_encoding)

    bid_jacks_teammate = get_bid_jacks(state['bid_jacks'][teammate_id])

    obs = np.concatenate((current_hand,  # 32
                            others_hand,  # 32
                            trick1,  # 32
                            trick2,  # 32
                            all_actions,  # 32*30
                            missing_cards_solo,  # 32
                            soloplayer_played_cards,  # 32
                            missing_cards_teammate,  # 32
                            teammate_played_cards,  # 32
                            last_soloplayer_action,  # 32
                            last_teammate_action,  # 32
                            points_own,  # 121
                            points_opp,  # 121
                            bid_teammate, # 5
                            bid_jacks_teammate, # 5
                            blind_hand))  # 1
    return obs

def extract_state(state, legal_actions):
    if state['self'] == state['soloplayer']:
        obs = get_soloplayer_features(state)
    else:
        obs = get_opponent_features(state)
    extracted_state = OrderedDict({'obs': obs, 'legal_actions': legal_actions})
    extracted_state['raw_obs'] = state
    extracted_state['raw_legal_actions'] = [a for a in state['actions']]
    return extracted_state
