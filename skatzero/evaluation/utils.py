import functools

from skatzero.game.utils import card_suit_as_number, card_rank_as_number

def skat_sort_card_string(card_1, card_2):
    key = []
    for card in [card_1, card_2]:
        key.append((card_suit_as_number[card[0]] * 10) + card_rank_as_number[card[1]])
        if card[1] == "J":
            key[-1] *= -1
    if key[0] > key[1]:
        return 1
    if key[0] < key[1]:
        return -1
    return 0


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


def format_hand(cards):
    cards.sort(key=functools.cmp_to_key(skat_sort_card_string))

    hand = ""
    for c in cards:
        hand += format_card(c) + " \033[0m"
    return hand
