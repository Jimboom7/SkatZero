from collections import OrderedDict

import numpy as np

card_encoding = {'D': 0, 'H': 1, 'S': 2, 'C': 3} # TODO: Make flexible
card_rank_to_column = {'7': 0, '8': 1, '9': 2, 'Q': 3, 'K': 4, 'T': 5, 'A': 6, 'J': 7}

def card2array(card):
    matrix = np.zeros([4, 8], dtype=np.int8)
    if card is None or card == '':
        return matrix.flatten()
    matrix[card_encoding[card[0]], card_rank_to_column[card[1]]] = 1
    return matrix.flatten()

def cards2array(cards):
    matrix = np.zeros([4, 8], dtype=np.int8)
    if cards is None or cards == ['']:
        return matrix.flatten()
    for card in cards:
        matrix[card_encoding[card[0]], card_rank_to_column[card[1]]] = 1
    return matrix.flatten()

def get_points_as_one_hot_vector(points, max_points=120):
    one_hot = np.zeros(max_points + 1, dtype=np.int8)
    one_hot[points] = 1
    return one_hot

def action_seq2array(action_seq_list):
    action_seq_array = np.zeros((len(action_seq_list), 32), np.int8)
    for row, card in enumerate(action_seq_list):
        action_seq_array[row, :] = card2array(card)
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

def calculate_missing_cards(player_id, trace, trump):
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

def get_common_features(state):
    current_hand = cards2array(state['current_hand'])
    others_hand = cards2array(state['others_hand'])

    all_actions = action_seq2array(process_action_seq(state['trace']))

    trick1 = card2array(None)
    trick2 = card2array(None)
    if len(state['trick']) >= 1:
        trick1 = card2array(state['trick'][0][1])
    if len(state['trick']) == 2:
        trick2 = card2array(state['trick'][1][1])
    return current_hand, others_hand, all_actions, trick1, trick2

def get_soloplayer_features(state, game):
    current_hand, others_hand, all_actions, trick1, trick2 = get_common_features(state)

    opponent_left_played_cards = cards2array(state['played_cards'][2])
    opponent_right_played_cards = cards2array(state['played_cards'][1])

    missing_cards_left = calculate_missing_cards(2, state['trace'], game.round.trump)
    missing_cards_right = calculate_missing_cards(1, state['trace'], game.round.trump)

    points_own = get_points_as_one_hot_vector(state['points'][0])
    points_opp = get_points_as_one_hot_vector(state['points'][1])

    skat = cards2array([game.round.dealer.skat[0], game.round.dealer.skat[1]])
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
                            points_opp))  # 121
    return obs

def get_opponent_features(state, game):
    current_hand, others_hand, all_actions, trick1, trick2 = get_common_features(state)
    soloplayer_played_cards = cards2array(state['played_cards'][0])
    for i, action in reversed(state['trace']):
        if i == state['soloplayer']:
            last_soloplayer_action = action
            break
    last_soloplayer_action = card2array(last_soloplayer_action)

    teammate_id = 3 - state['self']

    missing_cards_solo = calculate_missing_cards(0, state['trace'], game.round.trump)
    missing_cards_teammate = calculate_missing_cards(teammate_id, state['trace'], game.round.trump)

    points_own = get_points_as_one_hot_vector(state['points'][1])
    points_opp = get_points_as_one_hot_vector(state['points'][0])

    teammate_played_cards = cards2array(state['played_cards'][teammate_id])
    last_teammate_action = None
    for i, action in reversed(state['trace']):
        if i == teammate_id:
            last_teammate_action = action
            break
    last_teammate_action = card2array(last_teammate_action)
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
                            points_opp))  # 121
    return obs

def extract_state(state, game, legal_actions, action_recorder):
    if state['self'] == state['soloplayer']:
        obs = get_soloplayer_features(state, game)
    else:
        obs = get_opponent_features(state, game)
    extracted_state = OrderedDict({'obs': obs, 'legal_actions': legal_actions})
    extracted_state['raw_obs'] = state
    extracted_state['raw_legal_actions'] = [a for a in state['actions']]
    extracted_state['action_record'] = action_recorder
    return extracted_state
