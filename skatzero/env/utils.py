from collections import Counter
from operator import itemgetter
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


def calculate_bidding_value(cards, trump):
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
    # Ignore everything higher than this for now
    return val * mult

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

def evaluate_hand_strength(cards, suits = ['D','H','S','C']):
    '''
        Evaluate the strength of the hand
        Return the strength value and the best suit
    '''
    strength = []
    for suit in suits:
        s = 0
        for c in cards:
            s += evaluate_card(c, suit)
            strength.append((suit, s))
    return strength

def get_bids(basic_cards, min_value=8):
    bids = {'0': 0, '1': 0, '2': 0}
    for i in range(0, 3):
        strength = evaluate_hand_strength(basic_cards[str(i)])
        max_strength = max(strength, key=itemgetter(1))[1]
        if max_strength >= min_value:
            bids[str(i)] = calculate_bidding_value(basic_cards[str(i)], 'H') # Doesn't matter which trump we use for bid
    return bids

def get_hand_distribution(basic_cards):
    bids = get_bids(basic_cards, min_value=8)
    bid_order = dict(sorted(bids.items(), key=lambda item: item[1]))

    highest_bidder_wins = random.randint(1, 10) <= 8 # 80% for the highest bidder to win, otherwise second place will play
    if highest_bidder_wins:
        strongest = list(bid_order)[2]
    else:
        strongest = list(bid_order)[1]
        if bid_order[strongest] == 0:
            strongest = list(bid_order)[2]
    trump = get_suit_to_play(basic_cards[str(strongest)])

    card_play_data = {}
    card_play_data['skat_cards'] = basic_cards['skat_cards']
    card_play_data['suit'] = trump
    card_play_data['hand'] = basic_cards['hand']
    card_play_data['0'] = basic_cards[str(strongest)]
    card_play_data['1'] = basic_cards[str((int(strongest) + 1) % 3)]
    card_play_data['2'] = basic_cards[str((int(strongest) + 2) % 3)]
    card_play_data['bids'] = bids
    card_play_data['startplayer'] = get_startplayer()
    if not basic_cards['hand']:
        card_play_data['0'], card_play_data['skat_cards'] = discard_skat(card_play_data['0'], basic_cards['skat_cards'], basic_cards['suit'])

    return card_play_data

def get_suit_to_play(cards):
    """
    Return a suit to play, with weigthed probability based on the strength of the suits.
    """
    playable_suits = [str for str in evaluate_hand_strength(cards) if str[1] >= 8]
    if len(playable_suits) == 0:
        return 'D'
    suit = random.choices(playable_suits, weights=[str[1] - 7.5 for str in playable_suits])
    return suit[0][0]


def get_startplayer():
    return random.choice(['soloplayer', 'opponent_left', 'opponent_right'])


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
