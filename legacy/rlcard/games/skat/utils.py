''' Skat utils
'''

import functools
import math


CARD_SUIT_STR = ['D', 'H', 'S', 'C']
CARD_SUIT_STR_INDEX = {'D': 0 , 'H': 1, 'S': 2, 'C': 3}

CARD_RANK_STR = ['7', '8', '9', 'Q', 'K', 'T', 'A', 'J']
CARD_RANK_STR_INDEX = {'7': 0, '8': 1, '9': 2, 'Q': 3, 'K': 4, 'T': 5, 'A': 6, 'J': 7}
CARD_RANK_STR_VALUE = {'7': 0, '8': 0, '9': 0, 'J': 2, 'Q': 3, 'K': 4, 'T': 10, 'A': 11}

def skat_sort_card(card_1, card_2):
    ''' Compare the rank of two cards of Card object

    Args:
        card_1 (object): object of Card
        card_2 (object): object of card
    '''
    key = []
    for card in [card_1, card_2]:
        key.append((CARD_SUIT_STR.index(card.suit) * 10) + CARD_RANK_STR_INDEX[card.rank])
    if key[0] > key[1]:
        return 1
    if key[0] < key[1]:
        return -1
    return 0

def skat_sort_card_string(card_1, card_2):
    ''' Compare the rank of two string cards

    Args:
        card_1 (object): object of Card
        card_2 (object): object of card
    '''
    key = []
    for card in [card_1, card_2]:
        key.append((CARD_SUIT_STR.index(card[1]) * 10) + CARD_RANK_STR_INDEX[card[0]])
        if card[0] == "J":
            key[-1] *= -1
    if key[0] > key[1]:
        return 1
    if key[0] < key[1]:
        return -1
    return 0

def cards2str(cards):
    ''' Get the corresponding string representation of cards

    Args:
        cards (list): list of Card objects

    Returns:
        string: string representation of cards
    '''
    response = ''
    for card in cards:
        response += card.rank + card.suit
    return response

def compare_cards(card1, card2, trump, current_suit):
    '''
        Compare two cards.
        Returns true if first card is higher.
    '''
    if card1[0] == "J" and card2[0] == "J": # Two Jacks
        return CARD_SUIT_STR_INDEX[card1[1]] > CARD_SUIT_STR_INDEX[card2[1]]
    if card1[0] == "J" or card2[0] == "J": # One Jack
        return card1[0] == "J"
    if (card1[1] != current_suit) != (card2[1] != current_suit): # Different suites
        return (card1[1] == current_suit and card2[1] != trump) or card1[1] == trump
    return is_card_higher(card1, card2)

def is_card_higher(card1, card2):
    '''
        Check if value of card1 is higher than card2
    '''
    return CARD_RANK_STR_INDEX[card1[0]] > CARD_RANK_STR_INDEX[card2[0]]

def get_points(card):
    return CARD_RANK_STR_VALUE[card[0]]

def id_2_action(id):
    try:
        return CARD_RANK_STR[id % 8] + CARD_SUIT_STR[math.floor(id / 8)]
    except:
        return id

def action_2_id(action):
    return CARD_RANK_STR_INDEX[action[0]] + CARD_SUIT_STR_INDEX[action[1]] * 8

def evalute_hand_strength(cards, trump='D'):
    strength = 0
    for c in cards:
        if c.rank == 'J':
            strength += 2
        if c.suit == trump and c.rank != 'J':
            strength += 1
        if c.rank == 'A':
            strength += 1
        if c.rank == 'T':
            strength += 0.5
    return strength

def print_hand(cards):
    list_cards = []
    i = 0
    for c in cards:
        if i % 2 == 0:
            list_cards.append(c)
        else:
            list_cards[-1] += c
        i += 1
    list_cards.sort(key=functools.cmp_to_key(skat_sort_card_string))

    old_suite = list_cards[0][1]
    hand = ""
    for c in list_cards:
        if c[0] == "J":
            if hand == "":
                hand += "\033[95mJ"
            hand += c[1]
            old_suite = "J"
        else:
            if old_suite == "J":
                hand += " "
                old_suite = c[1]
            if c[1] != old_suite:
                hand += old_suite + " "
                old_suite = c[1]
            if c[1] == "D":
                hand += "\033[33m"
            if c[1] == "H":
                hand += "\033[31m"
            if c[1] == "S":
                hand += "\033[30m"
            if c[1] == "C":
                hand += "\033[32m"
            hand += c[0]
    hand += list_cards[-1][1] +  "\033[0m"
    print("Hand: " + hand)
