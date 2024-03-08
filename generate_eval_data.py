import argparse
import pickle
import numpy as np

suit_list = ['D', 'H', 'S', 'C']
rank_list = ['7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
deck = [suit + rank for suit in suit_list for rank in rank_list]

def get_parser():
    parser = argparse.ArgumentParser(description='Skat: random data generator')
    parser.add_argument('--output', default='eval_data', type=str)
    parser.add_argument('--num_games', default=10000, type=int)
    return parser

def generate():
    _deck = deck.copy()
    np.random.shuffle(_deck)
    card_play_data = {'0': _deck[:10],
                        '1': _deck[10:20],
                        '2': _deck[20:30],
                        'skat_cards': _deck[30:32]
        }
    return card_play_data


if __name__ == '__main__':
    flags = get_parser().parse_args()
    output_pickle = flags.output + '.pkl'

    print("output_pickle:", output_pickle)
    print("Generating data...")

    data = []
    for _ in range(flags.num_games):
        data.append(generate())

    print("Saving pickle file...")
    with open(output_pickle,'wb') as g:
        pickle.dump(data,g,pickle.HIGHEST_PROTOCOL)
