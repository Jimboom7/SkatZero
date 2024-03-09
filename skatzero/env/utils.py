from collections import Counter
import random


Card2Number = {'7': 0, '8': 1, '9': 2, 'Q': 3, 'K': 4, 'T': 5, 'A': 6, 'J': 7}
Suit2Number = {'D': 0, 'H': 1, 'S': 2, 'C': 3}
CardValue = {'7': 0, '8': 0, '9': 0, 'J': 2, 'Q': 3, 'K': 4, 'T': 10, 'A': 11}
Suit2Value = {'D': 9, 'H': 10, 'S': 11, 'C': 12}


def compare_cards(card1, card2, trump, current_suit):
    '''
        Compare two cards.
        Returns true if first card is higher.
    '''
    if card1[1] == "J" and card2[1] == "J":  # Two Jacks
        return Suit2Number[card1[0]] > Suit2Number[card2[0]]
    if card1[1] == "J" or card2[1] == "J":  # One Jack
        return card1[1] == "J"
    if (card1[0] != current_suit) != (card2[0] != current_suit):  # Different suites
        return (card1[0] == current_suit and card2[0] != trump) or card1[0] == trump
    return is_card_higher(card1, card2)


def is_card_higher(card1, card2):
    '''
        Check if value of card1 is higher than card2
    '''
    return Card2Number[card1[1]] > Card2Number[card2[1]]


def get_points(card):
    return CardValue[card[1]]


def get_bid(cards, trump):
    val = Suit2Value[trump]
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
    # Ignore everything above this for now
    return val * mult


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

def evaluate_hand_strength(cards, rand=True):
    '''
        Evaluate the strength of the hand
        Return the strength value and the best suit
    '''
    best_strength = -1
    best_suit = 'D'
    for suit in ['D','H','S','C']:
        strength = 0
        for c in cards:
            strength += evaluate_card(c, suit)
            if rand: # Sometimes you have to play with a weaker hand, depending on the bid
                strength *= random.uniform(0.9, 1.1)
        if strength >= best_strength:
            best_strength = strength
            best_suit = suit
    return best_strength, best_suit


def discard_skat(hand, skat, trump):
    '''
        Discard the worst cards from hand+skat.
        Returns the best 10 cards and the 2 bad cards.
        Pretty simple algorithm with the main purpose
        of being fast, it does not need to find the
        perfect hand.
    '''
    all_cards = hand + skat

    weak = []
    strong_hand = all_cards
    worst_skat = []

    for card in all_cards:
        if evaluate_card(card, trump) == 0 or (card[1] == 'T' and card[0] != trump):
            weak.append(card)

    if len(weak) < 2:
        return hand, skat

    c = Counter(card[0] for card in weak)
    short_suit = c.most_common()[-1][0]

    for card in weak:
        if card[0] == short_suit and (card[1] != 'T' or card[0] + 'A' not in strong_hand):
            worst_skat.append(card)
            strong_hand.remove(card)
        if len(worst_skat) == 2:
            return strong_hand, worst_skat

    if len(worst_skat) == 1:
        if weak[0] not in worst_skat:
            strong_hand.remove(weak[0])
            worst_skat.append(weak[0])
        else:
            strong_hand.remove(weak[1])
            worst_skat.append(weak[1])
        return strong_hand, worst_skat

    if len(worst_skat) == 0 and len(weak) >= 2:
        strong_hand.remove(weak[0])
        worst_skat.append(weak[0])
        strong_hand.remove(weak[1])
        worst_skat.append(weak[1])
        return strong_hand, worst_skat

    return hand, skat
