import numpy as np

#card_encoding = {'D': 0, 'H': 1, 'S': 2, 'C': 3}
Card2Column = {'7': 0, '8': 1, '9': 2, 'Q': 3, 'K': 4, 'T': 5, 'A': 6, 'J': 7}

def cards2array(cards, card_encoding):
    """
    A utility function that transforms the actions, i.e.,
    A list of card strings into a card matrix of dim 4x8,
    flattened to 32 0 or 1 values in a row.
    """
    matrix = np.zeros([4, 8], dtype=np.int8)
    if cards is None or cards == ['']:
        return matrix.flatten()
    for c in cards:
        matrix[card_encoding[c[0]], Card2Column[c[1]]] = 1
    return matrix.flatten()

def action_seq_list2array(action_seq_list, card_encoding):
    """
    A utility function to encode the historical moves.
    We encode the historical 30 actions. If there is
    no 30 actions, we pad the features with 0. Since
    three moves is a round in Skat, we concatenate
    the representations for each consecutive three moves.
    Finally, we obtain a 10x96 matrix, which will be fed
    into LSTM for encoding.
    """
    action_seq_array = np.zeros((len(action_seq_list), 32))
    for row, card in enumerate(action_seq_list):
        action_seq_array[row, :] = cards2array([card], card_encoding)
    action_seq_array = action_seq_array.reshape(10, 96)
    return action_seq_array

def process_action_seq(sequence, length=30):
    """
    A utility function encoding historical moves. We
    encode 30 moves. If there is no 30 moves, we pad
    with zeros.
    """
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

def get_points_as_one_hot_vector(points, max_points=120):
    """
    Points as one hot vector with size 121
    """
    one_hot = np.zeros(max_points + 1, dtype=np.int8)
    one_hot[points] = 1
    return one_hot

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

def get_obs(infoset):
    """
    This function obtains observations with imperfect information
    from the infoset. It has three branches since we encode
    different features for different positions.
    
    This function will return dictionary named `obs`. It contains
    several fields. These fields will be used to train the model.
    One can play with those features to improve the performance.

    `position` is a string that can be soloplayer/opponent_right/opponent_left

    `x_batch` is a batch of features (excluding the historical moves).
    It also encodes the action feature

    `z_batch` is a batch of features with historical moves only.

    `legal_actions` is the legal moves

    `x_no_action`: the features (exluding the historical moves and
    the action features). It does not have the batch dim.

    `z`: same as z_batch but not a batch.
    """
    if infoset.player_position == 'soloplayer':
        return _get_obs_soloplayer(infoset)
    if infoset.player_position == 'opponent_left' or infoset.player_position == 'opponent_right':
        return _get_obs_opponent(infoset)
    raise ValueError('')

def _get_obs_common(infoset):
    if infoset.trump == 'D':
        card_encoding = {'D': 0, 'H': 1, 'S': 2, 'C': 3}
    if infoset.trump == 'H':
        card_encoding = {'H': 0, 'D': 1, 'S': 2, 'C': 3}
    if infoset.trump == 'S':
        card_encoding = {'S': 0, 'H': 1, 'D': 2, 'C': 3}
    if infoset.trump == 'C':
        card_encoding = {'C': 0, 'H': 1, 'S': 2, 'D': 3}
    # Put Trump in front. TODO: Order the rest by amount in player hand

    num_legal_actions = len(infoset.legal_actions)

    my_handcards = cards2array(infoset.player_hand_cards, card_encoding)
    other_handcards = cards2array(infoset.other_hand_cards, card_encoding)

    trick1 = cards2array(None, card_encoding)
    trick2 = cards2array(None, card_encoding)
    if len(infoset.trick) >= 1:
        trick1 = cards2array([infoset.trick[0][1]], card_encoding)
    if len(infoset.trick) == 2:
        trick2 = cards2array([infoset.trick[1][1]], card_encoding)

    soloplayer_points = get_points_as_one_hot_vector(
        infoset.score['soloplayer'])
    opponent_points = get_points_as_one_hot_vector(
        infoset.score['opponent'])

    my_handcards_batch = np.repeat(my_handcards[np.newaxis, :], num_legal_actions, axis=0)
    other_handcards_batch = np.repeat(other_handcards[np.newaxis, :], num_legal_actions, axis=0)
    trick1_batch = np.repeat(trick1[np.newaxis, :], num_legal_actions, axis=0)
    trick2_batch = np.repeat(trick2[np.newaxis, :], num_legal_actions, axis=0)
    soloplayer_points_batch = np.repeat(soloplayer_points[np.newaxis, :], num_legal_actions, axis=0)
    opponent_points_batch = np.repeat(opponent_points[np.newaxis, :], num_legal_actions, axis=0)

    my_action_batch = np.zeros(my_handcards_batch.shape)
    for j, action in enumerate(infoset.legal_actions):
        my_action_batch[j, :] = cards2array([action], card_encoding)

    z = action_seq_list2array(process_action_seq(infoset.card_play_action_seq), card_encoding)
    z_batch = np.repeat(z[np.newaxis, :, :], num_legal_actions, axis=0)

    if infoset.hand:
        hand = np.ones([1,], dtype=np.int8)
    else:
        hand = np.zeros([1,], dtype=np.int8)
    hand_batch = np.repeat(hand[np.newaxis, :], num_legal_actions, axis=0)

    return (num_legal_actions, my_handcards, my_handcards_batch, other_handcards, other_handcards_batch, trick1, trick1_batch, trick2, trick2_batch,
            my_action_batch, soloplayer_points, soloplayer_points_batch, opponent_points, opponent_points_batch, z, z_batch, hand, hand_batch, card_encoding)

def _get_obs_soloplayer(infoset):
    """
    Obtain the soloplayer features.
    """
    (num_legal_actions, my_handcards, my_handcards_batch, other_handcards, other_handcards_batch, trick1, trick1_batch, trick2, trick2_batch,
    my_action_batch, soloplayer_points, soloplayer_points_batch, opponent_points, opponent_points_batch, z, z_batch, hand, hand_batch, card_encoding) = _get_obs_common(infoset)

    if not infoset.hand:
        skat = cards2array(infoset.skat_cards, card_encoding)
    else:
        skat = cards2array(None, card_encoding)
    missing_cards_left = calculate_missing_cards('opponent_left', infoset.card_play_action_seq, infoset.trump, card_encoding)
    missing_cards_right = calculate_missing_cards('opponent_right', infoset.card_play_action_seq, infoset.trump, card_encoding)
    opponent_left_played_cards = cards2array(infoset.played_cards['opponent_left'], card_encoding)
    opponent_right_played_cards = cards2array(infoset.played_cards['opponent_right'], card_encoding)

    skat_batch = np.repeat(skat[np.newaxis, :], num_legal_actions, axis=0)
    opponent_left_played_cards_batch = np.repeat(opponent_left_played_cards[np.newaxis, :], num_legal_actions, axis=0)
    opponent_right_played_cards_batch = np.repeat(opponent_right_played_cards[np.newaxis, :], num_legal_actions, axis=0)
    missing_cards_left_batch = np.repeat(missing_cards_left[np.newaxis, :], num_legal_actions, axis=0)
    missing_cards_right_batch = np.repeat(missing_cards_right[np.newaxis, :], num_legal_actions, axis=0)

    x_batch = np.hstack((hand_batch,
                         my_handcards_batch,
                         other_handcards_batch,
                         trick1_batch,
                         trick2_batch,
                         skat_batch,
                         opponent_left_played_cards_batch,
                         opponent_right_played_cards_batch,
                         soloplayer_points_batch,
                         opponent_points_batch,
                         missing_cards_left_batch,
                         missing_cards_right_batch,
                         my_action_batch))
    x_no_action = np.hstack((hand,
                             my_handcards,
                             other_handcards,
                             trick1,
                             trick2,
                             skat,
                             opponent_left_played_cards,
                             opponent_right_played_cards,
                             soloplayer_points,
                             opponent_points,
                             missing_cards_left,
                             missing_cards_right))

    obs = {
            'position': 'soloplayer',
            'x_batch': x_batch.astype(np.float32),
            'z_batch': z_batch.astype(np.float32),
            'legal_actions': infoset.legal_actions,
            'x_no_action': x_no_action.astype(np.int8),
            'z': z.astype(np.int8),
            'card_encoding': card_encoding
          }
    return obs

def _get_obs_opponent(infoset):
    """
    Obttain the opponent features.
    """

    teammate = 'opponent_left'
    if infoset.player_position == 'opponent_left':
        teammate = 'opponent_right'

    (num_legal_actions, my_handcards, my_handcards_batch, other_handcards, other_handcards_batch, trick1, trick1_batch, trick2, trick2_batch,
    my_action_batch, soloplayer_points, soloplayer_points_batch, opponent_points, opponent_points_batch, z, z_batch, hand, hand_batch, card_encoding) = _get_obs_common(infoset)

    last_soloplayer_action = cards2array([infoset.last_move_dict['soloplayer']], card_encoding)
    last_teammate_action = cards2array([infoset.last_move_dict[teammate]], card_encoding)
    soloplayer_played_cards = cards2array(infoset.played_cards['soloplayer'], card_encoding)
    teammate_played_cards = cards2array(infoset.played_cards[teammate], card_encoding)
    missing_cards_soloplayer = calculate_missing_cards('soloplayer', infoset.card_play_action_seq, infoset.trump, card_encoding)
    missing_cards_teammate = calculate_missing_cards(teammate, infoset.card_play_action_seq, infoset.trump, card_encoding)

    last_soloplayer_action_batch = np.repeat(last_soloplayer_action[np.newaxis, :],num_legal_actions, axis=0)
    last_teammate_action_batch = np.repeat(last_teammate_action[np.newaxis, :], num_legal_actions, axis=0)
    soloplayer_played_cards_batch = np.repeat(soloplayer_played_cards[np.newaxis, :],num_legal_actions, axis=0)
    teammate_played_cards_batch = np.repeat(teammate_played_cards[np.newaxis, :], num_legal_actions, axis=0)
    missing_cards_soloplayer_batch = np.repeat(missing_cards_soloplayer[np.newaxis, :], num_legal_actions, axis=0)
    missing_cards_teammate_batch = np.repeat(missing_cards_teammate[np.newaxis, :], num_legal_actions, axis=0)


    x_batch = np.hstack((hand_batch,
                         my_handcards_batch,
                         other_handcards_batch,
                         trick1_batch,
                         trick2_batch,
                         soloplayer_played_cards_batch,
                         teammate_played_cards_batch,
                         soloplayer_points_batch,
                         opponent_points_batch,
                         last_soloplayer_action_batch,
                         last_teammate_action_batch,
                         missing_cards_soloplayer_batch,
                         missing_cards_teammate_batch,
                         my_action_batch))
    x_no_action = np.hstack((hand,
                             my_handcards,
                             other_handcards,
                             trick1,
                             trick2,
                             soloplayer_played_cards,
                             teammate_played_cards,
                             soloplayer_points,
                             opponent_points,
                             last_soloplayer_action,
                             last_teammate_action,
                             missing_cards_soloplayer,
                             missing_cards_teammate))

    obs = {
            'position': infoset.player_position,
            'x_batch': x_batch.astype(np.float32),
            'z_batch': z_batch.astype(np.float32),
            'legal_actions': infoset.legal_actions,
            'x_no_action': x_no_action.astype(np.int8),
            'z': z.astype(np.int8),
            'card_encoding': card_encoding
          }
    return obs
