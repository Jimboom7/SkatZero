import argparse
import pickle
import numpy as np

from skatzero.env.utils import evaluate_hand_strength, get_hand_distribution

suit_list = ['D', 'H', 'S', 'C']
rank_list = ['7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
deck = [suit + rank for suit in suit_list for rank in rank_list]

def get_parser():
    parser = argparse.ArgumentParser(description='Skat: random data generator')
    parser.add_argument('--output', default='eval_data', type=str)
    parser.add_argument('--num_games', default=10000, type=int)
    parser.add_argument('--blind_hand_chance', default=0, type=float)
    return parser

def generate(quality, blind_hand_chance):
    _deck = deck.copy()
    np.random.shuffle(_deck)
    card_play_data = {'0': _deck[:10],
                        '1': _deck[10:20],
                        '2': _deck[20:30],
                        'skat_cards': _deck[30:32],
                        'suit': 'D',
                        'hand': np.random.random() < blind_hand_chance
        }
    if quality == 'bad':
        return card_play_data
    elif quality == 'medium':
        strongest = 0
        s0 = evaluate_hand_strength(card_play_data['0'], ['D'])[0][1]
        s1 = evaluate_hand_strength(card_play_data['1'], ['D'])[0][1]
        s2 = evaluate_hand_strength(card_play_data['2'], ['D'])[0][1]
        if s1 > s0 and s1 > s2:
            strongest = 1
        if s2 > s1 and s2 > s0:
            strongest = 2

        cards = {}
        cards['0'] = card_play_data[str(strongest)]
        cards['1'] = card_play_data[str((strongest + 1) % 3)]
        cards['2'] = card_play_data[str((strongest + 2) % 3)]
        cards['suit'] = card_play_data['suit']
        cards['hand'] = card_play_data['hand']
        cards['skat_cards'] = card_play_data['skat_cards']
    else:
        cards = get_hand_distribution(card_play_data)

    return cards


if __name__ == '__main__':
    flags = get_parser().parse_args()

    for quality in ['bad', 'medium', 'good']:
        output_pickle = flags.output + '_' + quality + '_' + str(flags.blind_hand_chance) + '.pkl'
        print("output_pickle:", output_pickle)
        print("Generating data...")
        data = []
        for _ in range(flags.num_games):
            data.append(generate(quality, flags.blind_hand_chance))

        print("Saving pickle file...")
        with open(output_pickle,'wb') as g:
            pickle.dump(data,g,pickle.HIGHEST_PROTOCOL)
