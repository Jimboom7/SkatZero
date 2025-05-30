from collections import OrderedDict

import numpy as np

from skatzero.game.utils import card_rank_as_number, card_ranks

jack_encoding = {'C': 0, 'S': 1, 'H': 2, 'D': 3}

def convert_action_id_to_card(action_id, card_encoding):
    if action_id < 100:
        if action_id % 8 == 7: # Jack
            return list(jack_encoding.keys())[list(jack_encoding.values()).index(int(action_id / 8))] + card_ranks[action_id % 8]
        return list(card_encoding.keys())[list(card_encoding.values()).index(int(action_id / 8))] + card_ranks[action_id % 8]
    else:
        return [convert_action_id_to_card(int(action_id / 100) - 1, card_encoding), convert_action_id_to_card(action_id % 100, card_encoding)]

def convert_card_to_action_id(action, card_encoding):
    if isinstance(action, str):
        if action[1] == 'J':
            return (jack_encoding[action[0]] * 8) + card_rank_as_number[action[1]]
        return (card_encoding[action[0]] * 8) + card_rank_as_number[action[1]]
    else:
        return ((convert_card_to_action_id(action[0], card_encoding) + 1) * 100) + convert_card_to_action_id(action[1], card_encoding)

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
    if number <= max_points:
        one_hot[number] = 1
    else:
        one_hot[-1] = 1
    return one_hot

def action_seq2array(action_seq_list, card_encoding):
    action_seq_array = np.zeros((len(action_seq_list), 35), np.int8)
    for row, action in enumerate(action_seq_list):
        if action[0] != -1:
            action_seq_array[row, 0:3] = get_number_as_one_hot_vector(action[0], 2)
        action_seq_array[row, 3:] = card2array(action[1], card_encoding)
    action_seq_array = action_seq_array.flatten()
    return action_seq_array

def process_action_seq(sequence, player_id, length=30):
    #sequence = [action[1] for action in sequence[-length:]]
    sequence = sequence.copy()
    if len(sequence) % 3 == 1:
        sequence.append((player_id, ''))
        sequence.append(((player_id + 1) % 3, ''))
    if len(sequence) % 3 == 2:
        sequence.append((player_id, ''))
    if len(sequence) < length:
        empty_sequence = [(-1, '') for _ in range(length - len(sequence))]
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
        if trick_counter % 3 == 0 or (trick_counter % 3 == 2 and len(trace) == trick_counter):
            if (player_card[0] == base_card[0]
                or ((((player_card[1] == 'J' or player_card[0] == trump) and
                    (base_card[1] == 'J' or base_card[0] == trump))) and trump is not None)):
                continue
            if (base_card[1] == 'J' and trump is not None) or base_card[0] == trump:
                if trump != 'J': # Grand
                    matrix[card_encoding[trump], :7] = 1
                matrix[:, 7] = 1
            else:
                matrix[card_encoding[base_card[0]], :7] = 1
                if trump is None: # Null
                    matrix[jack_encoding[base_card[0]], 7] = 1
    return matrix.flatten()

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

def get_card_encoding(state):
    global jack_encoding
    encoding = {}
    encoding_values = {'D': 0, 'H': 1, 'S': 2, 'C': 3}

    for x in ['D', 'H', 'S', 'C']:
        if state['trump'] is None:
            encoding_values[x] = ((len([d for d in state['current_hand'] if d[0] == x]) * 100) -
                    (len([d for d in state['others_hand'] if d[0] == x]) * 10) -
                    int(x + '7' in state['current_hand']))
        else:
            encoding_values[x] = ((len([d for d in state['current_hand'] if d[0] == x and d[1] != 'J']) * 100) -
                    (len([d for d in state['others_hand'] if d[0] == x and d[1] != 'J']) * 10) +
                    int(x + 'A' in state['current_hand']))

    if state['trump'] == 'D':
        encoding_values['D'] = 10000

    values = {'D': encoding_values['D'], 'H': encoding_values['H'], 'S': encoding_values['S'], 'C': encoding_values['C']}

    sorted_values = {k: v for k, v in sorted(values.items(), key=lambda item: item[1], reverse=True)}
    for i, k in enumerate(sorted_values):
        encoding[k] = i

    if state['trump'] is None:
        jack_encoding = encoding
    else:
        jack_encoding = {'C': 0, 'S': 1, 'H': 2, 'D': 3}

    return encoding

def get_common_features(state):
    card_encoding = get_card_encoding(state)
    current_hand = cards2array(state['current_hand'], card_encoding)
    others_hand = cards2array(state['others_hand'], card_encoding)

    all_actions = action_seq2array(process_action_seq(state['trace'], state['self']), card_encoding)

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

    opponent_left_played_cards = cards2array(state['played_cards'][1], card_encoding)
    opponent_right_played_cards = cards2array(state['played_cards'][2], card_encoding)

    missing_cards_left = calculate_missing_cards(1, state['trace'], state['trump'], card_encoding)
    missing_cards_right = calculate_missing_cards(2, state['trace'], state['trump'], card_encoding)

    points_own = get_number_as_one_hot_vector(state['points'][0])
    points_opp = get_number_as_one_hot_vector(state['points'][1])

    drueck = np.zeros([1,], dtype=np.int8)
    pos = np.zeros([3,], dtype=np.int8)
    if state["drueck"]:
        drueck[0] = 1
        pos[state["pos"]] = 1

    bid_left = get_bid(state['bids'][1], card_encoding)
    bid_right = get_bid(state['bids'][2], card_encoding)

    bid_jacks_left = get_bid_jacks(state['bid_jacks'][1])
    bid_jacks_right = get_bid_jacks(state['bid_jacks'][2])

    if not state['blind_hand'] and len(state['skat']) == 2:
        skat = cards2array([state['skat'][0], state['skat'][1]], card_encoding)
    else:
        skat = cards2array(None, card_encoding)

    history = all_actions

    obs = np.concatenate((current_hand,  # 32
                            others_hand,  # 32
                            trick1,  # 32
                            trick2,  # 32
                            skat,  # 32
                            missing_cards_left,  # 32
                            opponent_left_played_cards,  # 32
                            missing_cards_right,  # 32
                            opponent_right_played_cards,  # 32
                            points_own,  # 121
                            points_opp, # 121
                            drueck, # 1
                            pos, # 3
                            bid_left, # 5
                            bid_right, # 5
                            bid_jacks_left, # 5
                            bid_jacks_right, # 5
                            blind_hand)) # 1

    if state['trump'] is None: # Null
        if state['open_hand']:
            open_hand = np.ones([1,], dtype=np.int8)
        else:
            open_hand = np.zeros([1,], dtype=np.int8)
        obs = np.concatenate((current_hand,  # 32
                                others_hand,  # 32
                                trick1,  # 32
                                trick2,  # 32
                                skat,  # 32
                                missing_cards_left,  # 32
                                opponent_left_played_cards,  # 32
                                missing_cards_right,  # 32
                                opponent_right_played_cards,  # 32
                                bid_left, # 5
                                bid_right, # 5
                                bid_jacks_left, # 5
                                bid_jacks_right, # 5
                                blind_hand, # 1
                                open_hand, # 1
                                drueck, # 1
                                pos )) # 3

    return obs, history

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

    history = all_actions

    obs = np.concatenate((current_hand,  # 32
                            others_hand,  # 32
                            trick1,  # 32
                            trick2,  # 32
                            missing_cards_solo,  # 32
                            soloplayer_played_cards,  # 32
                            missing_cards_teammate,  # 32
                            teammate_played_cards,  # 32
                            last_soloplayer_action,  # 32
                            last_teammate_action,  # 32
                            points_own,  # 121
                            points_opp,  # 121
                            bid_teammate,  # 5
                            bid_jacks_teammate,  # 5
                            blind_hand))  # 1

    if state['trump'] is None: # Null
        if state['open_hand']:
            open_hand = np.ones([1,], dtype=np.int8)
            soloplayer_open_cards = cards2array(state['soloplayer_open_cards'], card_encoding)
        else:
            open_hand = np.zeros([1,], dtype=np.int8)
            soloplayer_open_cards = cards2array(None, card_encoding)
        obs = np.concatenate((current_hand,  # 32
                                others_hand,  # 32
                                trick1,  # 32
                                trick2,  # 32
                                missing_cards_solo,  # 32
                                soloplayer_played_cards,  # 32
                                missing_cards_teammate,  # 32
                                teammate_played_cards,  # 32
                                last_soloplayer_action,  # 32
                                last_teammate_action,  # 32
                                soloplayer_open_cards,  # 32
                                bid_teammate,  # 5
                                bid_jacks_teammate,  # 5
                                blind_hand,  # 1
                                open_hand))  # 1

    return obs, history

def extract_state(state, legal_actions):
    if state['self'] == state['soloplayer']:
        obs, history = get_soloplayer_features(state)
    else:
        obs, history = get_opponent_features(state)
    extracted_state = OrderedDict({'obs': obs, 'legal_actions': legal_actions})
    history = history.reshape(10, 105)
    extracted_state['history'] = history
    extracted_state['raw_obs'] = state
    extracted_state['raw_legal_actions'] = [a for a in state['actions']]
    # print(extracted_state)
    return extracted_state
