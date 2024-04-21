import matplotlib.pyplot as plt

from skatzero.evaluation.utils import format_card
from skatzero.evaluation.simulation import prepare_env
from bidding.bidder_advanced import AdvancedBidder

if __name__ == '__main__':

    env, raw_state = prepare_env(False)
    raw_state['skat'] = []
    bidder = AdvancedBidder(env, raw_state)

    hand_cards = bidder.get_hand_cards()
    for card in hand_cards:
        print(f'{format_card(card)}')
    hand_estimates = bidder.get_blind_hand_values()
    print('Handspiel-Erwartungswerte:')
    suits = ['♣', '♠', '♥', '♦', 'G', 'N', 'NO']
    for ind, suit in enumerate(suits):
        print(f'{suit}: {hand_estimates[ind]}')


    colors = ['green', 'mediumblue', 'red', 'darkorange', 'black', 'pink', 'purple']
    plt.ion()  # turning interactive mode on
    for ind, color in enumerate(colors):
        line = plt.plot([1, 231], [hand_estimates[ind], hand_estimates[ind]], '--', color=color, label=f'{suits[ind]} Hand')[0]
        #line.set_label(f'{suits[ind]} Hand')
    plt.ylim(-200, 100)
    plt.xlabel('Geprüfte Skats')
    plt.ylabel('Erwartungswert nach Seeger-Fabian')
    plt.pause(0.05)

    means_over_skats = {'C': [], 'S': [], 'H': [], 'D': [], 'G': [], 'N': [], 'NO': []}
    graphs = [None] * 7
    for i in range(231):
        mean_estimates, bid_value_table = bidder.update_value_estimates()
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
    for game_mode in means_over_skats.keys():
        print(game_mode + ": " +str(sum(mean_estimates[game_mode]) / len(mean_estimates[game_mode])))

    #info = get_bidding_data(MODEL, True)

    #sorted_info = dict(sorted(info.items(), key=lambda item: item[1], reverse=True))

    #for action, value in sorted_info.items():
    #    print(format_card(action) + ": " + str(value))
