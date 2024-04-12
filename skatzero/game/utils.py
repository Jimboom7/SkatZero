import random


card_suits = ['D', 'H', 'S', 'C']
card_suit_as_number = {'D': 0 , 'H': 1, 'S': 2, 'C': 3}

card_ranks = ['7', '8', '9', 'Q', 'K', 'T', 'A', 'J']
card_rank_as_number = {'7': 0, '8': 1, '9': 2, 'Q': 3, 'K': 4, 'T': 5, 'A': 6, 'J': 7}
card_point_value = {'7': 0, '8': 0, '9': 0, 'J': 2, 'Q': 3, 'K': 4, 'T': 10, 'A': 11}

def init_32_deck():
    res = [suit + rank for suit in card_suits for rank in card_ranks]
    return res

def compare_cards(card1, card2, trump, current_suit): # TODO: Für Null anpassen
    if card1[1] == "J" and card2[1] == "J": # Two Jacks
        return card_suit_as_number[card1[0]] > card_suit_as_number[card2[0]]
    if card1[1] == "J" or card2[1] == "J": # One Jack
        return card1[1] == "J"
    if card1[0] != card2[0]: # Different suites
        if trump == 'J': # Grand
            return card1
        return (card1[0] == current_suit and card2[0] != trump) or card1[0] == trump
    return is_card_higher(card1, card2)


def is_card_higher(card1, card2):
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


def evaluate_hand_strength(cards, gametype = ['D', 'H', 'S', 'C'], np_random=None):
    if gametype == 'G':
        strength = 0
        for c in cards:
            strength += evaluate_grand_card(c)
        if np_random is None:
            return {'G': strength}
        return {'G': strength * np_random.uniform(0.85, 1.15)}
    strength = {'D': 0, 'H': 0, 'S': 0, 'C': 0}
    for suit in gametype:
        s = 0
        for c in cards:
            s += evaluate_card(c, suit)
        if np_random is None:
            strength[suit] = s
        else:
            strength[suit] = s * np_random.uniform(0.9, 1.1)
    return strength


def can_play_null(cards):
    nullcards = 0
    for card in cards:
        if card[1] == '7':
            nullcards += 1
        if card[1] == '8':
            nullcards += 0.8
        if card[1] == '9':
            nullcards += 0.6
        if card[1] == 'T':
            nullcards += 0.4
        if card[1] == 'J':
            nullcards += 0.2
        if card[1] == 'K':
            nullcards -= 0.2
        if card[1] == 'A':
            nullcards -= 0.4
    return nullcards > 5
