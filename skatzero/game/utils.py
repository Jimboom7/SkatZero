card_suits = ['D', 'H', 'S', 'C']
card_suit_as_number = {'D': 0 , 'H': 1, 'S': 2, 'C': 3}

card_ranks = ['7', '8', '9', 'Q', 'K', 'T', 'A', 'J']
card_rank_as_number = {'7': 0, '8': 1, '9': 2, 'Q': 3, 'K': 4, 'T': 5, 'A': 6, 'J': 7}
card_rank_as_number_null = {'7': 0, '8': 1, '9': 2, 'T': 3, 'J': 4, 'Q': 5, 'K': 6, 'A': 7}
card_point_value = {'7': 0, '8': 0, '9': 0, 'J': 2, 'Q': 3, 'K': 4, 'T': 10, 'A': 11}

def init_32_deck():
    res = [suit + rank for suit in card_suits for rank in card_ranks]
    return res

def compare_cards(card1, card2, trump, current_suit):
    if trump is not None and (card1[1] == "J" and card2[1] == "J"): # Two Jacks
        return card_suit_as_number[card1[0]] > card_suit_as_number[card2[0]]
    if trump is not None and (card1[1] == "J" or card2[1] == "J"): # One Jack
        return card1[1] == "J"
    if card1[0] != card2[0]: # Different suites
        if trump == 'J' or trump is None: # Grand or Null
            return True
        return (card1[0] == current_suit and card2[0] != trump) or card1[0] == trump
    return is_card_higher(card1, card2, trump)


def is_card_higher(card1, card2, trump):
    if trump is None: # Null
        return card_rank_as_number_null[card1[1]] > card_rank_as_number_null[card2[1]]
    return card_rank_as_number[card1[1]] > card_rank_as_number[card2[1]]


def get_points(card):
    return card_point_value[card[1]]


def calculate_bidding_value(cards):
    mult = 2
    if 'CJ' in cards and 'SJ' in cards:
        mult = 3
    if 'CJ' not in cards and 'SJ' not in cards:
        mult = 3
    if 'CJ' in cards and 'SJ' in cards and 'HJ' in cards:
        mult = 4
    if 'CJ' not in cards and 'SJ' not in cards and 'HJ' not in cards:
        mult = 4
    if 'CJ' in cards and 'SJ' in cards and 'HJ' in cards and 'DJ' in cards:
        mult = 5
    if 'CJ' not in cards and 'SJ' not in cards and 'HJ' not in cards and 'DJ' not in cards:
        mult = 5
    # Ignore everything higher than this for now
    return mult


def calculate_max_bids(cards, gamemode):
    base_values = {'G': 24, 'C': 12, 'S': 11, 'H': 10, 'D': 9}
    gametype = gamemode[0]
    is_hand = True if len(gamemode) > 1 else False

    if 'CJ' in cards:
        if 'SJ' in cards:
            if 'HJ' in cards:
                if 'DJ' in cards:
                    if gametype != 'G' and (gametype + 'A') in cards:
                        if (gametype + 'T') in cards:
                            if (gametype + 'K') in cards:
                                if (gametype + 'Q') in cards:
                                    if (gametype + '9') in cards:
                                        if (gametype + '8') in cards:
                                            if (gametype + '7') in cards:
                                                mult = 12
                                            else:
                                                mult = 11
                                        else:
                                            mult = 10
                                    else:
                                        mult = 9
                                else:
                                    mult = 8
                            else:
                                mult = 7
                        else:
                            mult = 6
                    else:
                        mult = 5
                else:
                    mult = 4
            else:
                mult = 3
        else:
            mult = 2
    else:
        if 'SJ' not in cards:
            if 'HJ' not in cards:
                if 'DJ' not in cards:
                    if gametype != 'G' and (gametype + 'A') not in cards:
                        if (gametype + 'T') not in cards:
                            if (gametype + 'K') not in cards:
                                if (gametype + 'Q') not in cards:
                                    if (gametype + '9') not in cards:
                                        if (gametype + '8') not in cards:
                                            if (gametype + '7') not in cards:
                                                mult = 12
                                            else:
                                                mult = 11
                                        else:
                                            mult = 10
                                    else:
                                        mult = 9
                                else:
                                    mult = 8
                            else:
                                mult = 7
                        else:
                            mult = 6
                    else:
                        mult = 5
                else:
                    mult = 4
            else:
                mult = 3
        else:
            mult = 2

    if is_hand:
        mult += 1
    max_bids = {'Normal': mult*base_values[gametype], 'Schneider': (mult+1)*base_values[gametype], 'Schwarz': (mult+2)*base_values[gametype]}
    return max_bids



# Simplified von Stegen System, hand is playable at absolut minimum 7 points
def evaluate_card(card, trump):
    strength = 0
    if card[1] == 'J':
        strength += 2
    if card[0] == trump and card[1] != 'J':
        strength += 1
    if card[1] == 'A':
        strength += 1
    if card[1] == 'T':
        strength += 0.5
    return strength


def evaluate_grand_card(card):
    if card[1] == 'J':
        return 1
    if card[1] == 'A':
        return 1
    if card[1] == 'T':
        return 0.5
    return 0


def evaluate_hand_strength(cards, gametype = ['D', 'H', 'S', 'C'], np_random=None, more_random=False):
    rand_l = 0.7 if more_random else 0.9
    rand_u = 1.2 if more_random else 1.1
    if gametype == 'N':
        return {'N': evaluate_null_strength(cards, []) * np_random.uniform(rand_l, rand_u)}
    elif gametype == 'G':
        rand = 0.5 if more_random else 0.2
        strength = 0
        for c in cards:
            strength += evaluate_grand_card(c)
        if np_random is None:
            return {'G': strength}
        return {'G': strength * np_random.uniform(1 - rand, 1 + rand)}
    strength = {'D': 0, 'H': 0, 'S': 0, 'C': 0}
    for suit in gametype:
        s = 0
        for c in cards:
            s += evaluate_card(c, suit)
        if sum(card[0] == suit for card in cards) <= 4:
            s += 0.2 - (sum(card[0] == suit and (card[1] == 'T' or card[1] == 'A') for card in cards) / 5)
        if np_random is None:
            strength[suit] = s
        else:
            strength[suit] = s * np_random.uniform(rand_l, rand_u)
    return strength

def evaluate_d_strength_for_druecken(cards, skat, np_random=None):
    strength = 0
    for card in cards:
        expected_value = 0
        sum_suit = sum(card[0] in s and s[1] != 'J' for s in cards)
        sum_suit_total = sum(card[0] in s and s[1] != 'J' for s in cards + skat)
        sum_trump = sum(s[1] == 'J' or s[0] == 'D' for s in cards)
        if card == 'CJ':
            expected_value = 240
        if card == 'SJ':
            expected_value = 220
        if card == 'HJ':
            expected_value = 210
        if card == 'DJ':
            expected_value = 200

        if card[0] == 'D':
            expected_value = 180

        elif card[1] == 'A' or (card[1] == 'T' and card[0] + 'A' in cards + skat):
            expected_value = 100
            if sum_trump <= 4:
                if card[0] + 'T' in cards + skat:
                    if sum_suit_total == 4:
                        expected_value = 0
                    elif sum_suit_total >= 5:
                        expected_value = 0
                elif sum_suit_total >= 5:
                    expected_value = 0

        elif card[1] == 'T':
            if card[0] + 'K' in cards:
                expected_value = 9 - (np_random.rand() * 6)
                if sum_suit == 3:
                    expected_value = 9 - (np_random.rand() * 4)
            elif card[0] + 'Q' in cards:
                expected_value = 3 - (np_random.rand() * 2)
                if sum_suit == 3:
                    expected_value = 3 - (np_random.rand() * 1)
            else:
                if sum_suit == 1:
                    expected_value = -10
                elif sum_suit == 2:
                    expected_value = -3
                else:
                    expected_value = 0
            if sum_suit == 3:
                expected_value *= 1.2
            if sum_trump <= 4:
                if sum_suit_total >= 4:
                    expected_value = 0

        elif card[1] == 'K':
            if card[0] + 'A' in cards + skat and sum_suit >= 3:
                expected_value = 2.9
            else:
                expected_value = 0

        elif card[1] == 'Q':
            if card[0] + 'A' in cards + skat and sum_suit >= 3:
                expected_value = 3
                if card[0] + 'K' in skat:
                    expected_value -= 0.2
            else:
                expected_value = 0

        elif card[1] == '7' or card[1] == '8' or card[1] == '9':
            if sum_suit >= 3:
                expected_value = 0.1
            else:
                expected_value = 0

        if sum_trump >= 6 and sum_suit >= 4:
            expected_value += 5

        strength += expected_value

    for suit in ['H', 'S', 'C']:
        sum_suit = sum(suit in s and s[1] != 'J' for s in cards)
        if sum_suit == 0:
            if suit + 'A' not in skat:
                strength += (sum_trump - 3) * 3
            if suit + 'T' not in skat:
                strength += (sum_trump - 3) * 3
        if sum_suit == 1:
            strength += 2
            if suit + 'K' in cards:
                strength -= 1
            if suit + 'Q' in cards:
                strength -= 0.5
        if sum_suit == 2:
            if suit + 'A' not in cards:
                strength -= 5

        if suit + 'T' in cards and suit + 'K' in skat:
            strength -= 1000
        if suit + 'K' in cards and suit + 'Q' in skat:
            strength -= 1000
        if suit + 'Q' in cards and suit + '9' in skat:
            strength -= 1000

        if suit + 'A' in skat and suit + 'T' in skat and sum_suit == 2:
            strength -= 10

    if skat[0][0] == skat[1][0]:
        strength += 2

    strength += get_points(skat[0]) + get_points(skat[1])
    if skat[0][1] == 'A': # Fix to make A and T equally valuable
        strength -= 1
    if skat[1][1] == 'A':
        strength -= 1

    return strength

def evaluate_grand_strength_for_druecken(cards, skat, np_random=None):
    strength = 0
    for card in cards:
        expected_value = 0
        sum_suit = sum(card[0] in s and s[1] != 'J' for s in cards)
        sum_suit_total = sum(card[0] in s and s[1] != 'J' for s in cards + skat)
        sum_trump = sum(s[1] == 'J' for s in cards)
        if card == 'CJ':
            expected_value = 24
        if card == 'SJ':
            expected_value = 22
        if card == 'HJ':
            expected_value = 21
        if card == 'DJ':
            expected_value = 20

        if card[1] == 'A' or (card[1] == 'T' and card[0] + 'A' in skat):
            expected_value = 11
            if card[0] + 'T' not in cards + skat:
                expected_value += 3
            if card[0] + 'K' not in cards + skat:
                expected_value += 1
            if card[0] + 'Q' not in cards + skat:
                expected_value += 1
            if sum_suit_total <= 1:
                expected_value += 100
            if sum_trump <= 1:
                if card[0] + 'T' in cards + skat:
                    if sum_suit_total == 3:
                        expected_value = 3
                    elif sum_suit_total >= 4:
                        expected_value = 0
                elif sum_suit_total >= 5:
                    expected_value = 0

        elif card[1] == 'T':
            if card[0] + 'A' in cards + skat:
                expected_value = 10
                if card[0] + 'K' not in cards + skat:
                    expected_value += 1
                if card[0] + 'Q' not in cards + skat:
                    expected_value += 1
            else:
                if card[0] + 'K' in cards:
                    expected_value = 5 - (np_random.rand() * 3)
                    if sum_suit == 3:
                        expected_value = 5 - (np_random.rand() * 1.5)
                elif card[0] + 'Q' in cards:
                    expected_value = 3 - (np_random.rand() * 2)
                    if sum_suit == 3:
                        expected_value = 3 - (np_random.rand() * 1)
                else:
                    if sum_suit == 1:
                        expected_value = -10
                    elif sum_suit == 2:
                        expected_value = -3
                    else:
                        expected_value = 0
                if sum_suit == 3:
                    expected_value *= 1.2
            if sum_trump <= 1:
                if sum_suit_total >= 4:
                    expected_value = 0

        elif card[1] == 'K':
            if card[0] + 'A' in cards + skat and sum_suit >= 3:
                expected_value = 2.9
            else:
                expected_value = 0

        elif card[1] == 'Q':
            if card[0] + 'A' in cards + skat and sum_suit >= 3:
                expected_value = 3
                if card[0] + 'K' in skat:
                    expected_value -= 0.2
            else:
                expected_value = 0

        elif card[1] == '7' or card[1] == '8' or card[1] == '9':
            if sum_suit >= 3:
                expected_value = 0.1
            else:
                expected_value = 0

        if sum_trump >= 3 and sum_suit >= 4:
            expected_value += 5

        strength += expected_value

    for suit in ['D', 'H', 'S', 'C']:
        sum_suit = sum(suit in s and s[1] != 'J' for s in cards)
        if sum_suit == 0:
            if suit + 'A' not in skat:
                strength += (sum_trump - 1) * 3
            if suit + 'T' not in skat:
                strength += (sum_trump - 1) * 3
        if sum_suit == 1:
            strength += 2
            if suit + 'K' in cards:
                strength -= 1
            if suit + 'Q' in cards:
                strength -= 0.5

        if suit + 'T' in cards and suit + 'K' in skat:
            strength -= 1000
        if suit + 'K' in cards and suit + 'Q' in skat:
            strength -= 1000
        if suit + 'Q' in cards and suit + '9' in skat:
            strength -= 1000

    if skat[0][0] == skat[1][0]:
        strength += 2

    strength += get_points(skat[0]) + get_points(skat[1])
    if skat[0][1] == 'A': # Fix to make A and T equally valuable
        strength -= 1
    if skat[1][1] == 'A':
        strength -= 1

    return strength

"""
https://www.vg88.de/Download/_besser-Skat-spielen-V1b.pdf
Stufe 1: Das Ass zu viert, etwa 7-8-10-Ass oder 7-9-Bube-Ass
 Stufe 2: Die blanke 8
 Stufe 3: 7-10
 Stufe 4: 8-9 und (gleich schwach) die Dame zu dritt: 7-8-Dame bzw. 7-9-Dame
 Stufe 5: 8-10
 Stufe 6: Die blanke 9
 Stufe 7: 7-9-König bzw. 7-8-König
 """
def evaluate_null_strength(cards, skat = []):
    strength = 0
    for suit in ['D', 'H', 'S', 'C']:
        if sum(suit in s for s in cards) == 0:
            strength += 0
        elif (sum(suit in s for s in cards) == 4 and suit + '7' in cards and
        (suit + '8' in cards or suit + '9' in cards) and
        ((suit + '8' in cards and suit + '9' in cards) or suit + 'J' in cards or suit + 'Q' in cards or suit + 'K' in cards) and
        suit + 'A' in cards):
            strength += 1
        elif sum(suit in s for s in cards) == 1 and suit + '8' in cards:
            strength += 2
        elif sum(suit in s for s in cards) == 2 and suit + '7' in cards and suit + 'T' in cards:
            strength += 3
        elif sum(suit in s for s in cards) == 2 and suit + '8' in cards and suit + '9' in cards:
            strength += 4
        elif sum(suit in s for s in cards) == 3 and suit + '7' in cards and (suit + '8' in cards or suit + '9' in cards) and suit + 'Q' in cards:
            strength += 4
        elif sum(suit in s for s in cards) == 2 and suit + '8' in cards and suit + 'T' in cards:
            strength += 5
        elif sum(suit in s for s in cards) == 1 and suit + '9' in cards:
            strength += 6
        elif sum(suit in s for s in cards) == 3 and suit + '7' in cards and (suit + '8' in cards or suit + '9' in cards) and suit + 'K' in cards:
            strength += 7
        else:
            mod = 20
            filler = 0
            current_strength = 0
            for rank in ['7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                if mod < 6:
                    break
                if suit + rank in cards:
                    strength += current_strength
                    current_strength = 0
                    mod *= 0.6
                    filler += 1
                else:
                    if suit + rank in skat:
                        mod *= 0.8
                    if filler <= 0:
                        current_strength += mod
                    filler -= 1

    return -strength

def can_play_null(cards, gametype, np_random): # Bids more aggressive when the trained model is not a Null model. Otherwise there are not enough null bids.
    if gametype != 'N':
        return evaluate_null_strength(cards) >= -78
    return evaluate_null_strength(cards) >= -30 - np_random.uniform(0, 10)

def can_play_null_ouvert(cards, gametype, np_random):
    if gametype != 'N':
        return evaluate_null_strength(cards) >= -45
    return evaluate_null_strength(cards) >= -8 - np_random.uniform(0, 2.5)

def can_play_null_ouvert_hand(cards, gametype, np_random):
    if gametype != 'N':
        return evaluate_null_strength(cards) >= -5
    return evaluate_null_strength(cards) >= -2 - np_random.uniform(0, 2.2)
