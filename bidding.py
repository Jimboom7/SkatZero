import matplotlib.pyplot as plt

from skatzero.evaluation.utils import format_card
from skatzero.evaluation.simulation import get_bidding_data, prepare_env
from skatzero.evaluation.bidder import Bidder

if __name__ == '__main__':

    MODEL = "checkpoints/skat_D/0_6000.pth"

    env, raw_state = prepare_env(MODEL, False)
    raw_state['skat'] = []
    bidder = Bidder(env, raw_state)
    hand_cards = bidder.get_hand_cards()
    for card in hand_cards:
        print(f'{format_card(card)}')
    hand_estimates = bidder.get_blind_hand_values()
    print('Handspiel-Erwartungswerte:')
    suits = ['♣', '♠', '♥', '♦']
    for ind, suit in enumerate(suits):
        print(f'{suit}: {hand_estimates[ind]}')


    colors = ['green', 'mediumblue', 'red', 'darkorange']
    plt.ion()  # turning interactive mode on
    for ind, color in enumerate(colors):
        line = plt.plot([1, 231], [hand_estimates[ind], hand_estimates[ind]], '--', color=color, label=f'{suits[ind]} Hand')[0]
        #line.set_label(f'{suits[ind]} Hand')
    plt.ylim(-150, 100)
    plt.xlabel('Geprüfte Skats')
    plt.ylabel('Erwartungswert nach Seeger-Fabian')
    plt.pause(0.05)

    means_over_skats = {'C': [], 'S': [], 'H': [], 'D': []}
    graphs = [None] * 4
    for i in range(231):
        mean_estimates = bidder.update_value_estimates()
        for game_mode in means_over_skats.keys():
            means_over_skats[game_mode].append(sum(mean_estimates[game_mode]) / len(mean_estimates[game_mode]))
        try:
            for graph in graphs:
                graph.remove() 
        except:
            pass
        for ind, game_mode in enumerate(means_over_skats.keys()):
            graphs[ind] = plt.plot(list(range(1, i+2)), means_over_skats[game_mode], color=colors[ind], label=f'{suits[ind]}')
            #graphs[ind].set_label(f'{suits[ind]}')
        if i == 0:
            plt.legend(loc='upper right', prop={'size': 6})
        plt.pause(0.05)
            #print(f'Mit Skat-Erwartungswerte ({i+1} Skats geprüft):')
            #for ind, suit in enumerate(['♣', '♠', '♥', '♦']):
            #    print(f'{suit}: {}')

    #info = get_bidding_data(MODEL, True)

    #sorted_info = dict(sorted(info.items(), key=lambda item: item[1], reverse=True))

    #for action, value in sorted_info.items():
    #    print(format_card(action) + ": " + str(value))
