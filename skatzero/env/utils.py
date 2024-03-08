import functools


Card2Number = {'7': 0, '8': 1, '9': 2, 'Q': 3, 'K': 4, 'T': 5, 'A': 6, 'J': 7}
Suit2Number = {'D': 0, 'H': 1, 'S': 2, 'C': 3}
CardValue = {'7': 0, '8': 0, '9': 0, 'J': 2, 'Q': 3, 'K': 4, 'T': 10, 'A': 11}


def skat_sort_card_string(card_1, card_2):
    ''' Compare the rank of two string cards

    Args:
        card_1 (object): object of Card
        card_2 (object): object of card
    '''
    key = []
    for card in [card_1, card_2]:
        key.append((Suit2Number[card[0]] * 10) + Card2Number[card[1]])
        if card[1] == "J":
            key[-1] *= -1
    if key[0] > key[1]:
        return 1
    if key[0] < key[1]:
        return -1
    return 0


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


def evalute_hand_strength(cards, trump='D'):
    strength = 0
    for c in cards:
        if c[1] == 'J':
            strength += 2
        if c[0] == trump and c[1] != 'J':
            strength += 1
        if c[1] == 'A':
            strength += 1
        if c[1] == 'T':
            strength += 0.5
    return strength


def format_hand(cards):
    suits = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣' }

    cards.sort(key=functools.cmp_to_key(skat_sort_card_string))

    hand = ""
    for c in cards:
        hand += format_card(c) + " \033[0m"
    return hand

def format_card(card):
    suits = {'S': '♠', 'H': '♥', 'D': '♦', 'C': '♣' }

    output = ""
    if card[1] == "J":
        output += "\033[95m"
    elif card[0] == "D":
        output += "\033[33m"
    elif card[0] == "H":
        output += "\033[31m"
    elif card[0] == "S":
        output += "\033[34m"
    elif card[0] == "C":
        output += "\033[32m"

    if card[1] == "T":
        output += "10" + suits[card[0]] + "\033[0m"
    else:
        output += card[1] + suits[card[0]] + "\033[0m"
    
    return output
