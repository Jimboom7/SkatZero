import matplotlib.pyplot as plt
import numpy as np

import copy
from skatzero.env.skat import SkatEnv
from skatzero.evaluation.simulation import load_model
from bidding.bidder import Bidder

if __name__ == '__main__':

    gametype = 'G' # hier den Spieltyp einstellen
    is_hand = True

    MODEL1_D = 'models/latest/D_0.pth'
    MODEL2_D = 'models/latest/D_1.pth'
    MODEL3_D = 'models/latest/D_2.pth'
    MODEL1_G = 'models/latest/G_0.pth'
    MODEL2_G = 'models/latest/G_1.pth'
    MODEL3_G = 'models/latest/G_2.pth'

    if gametype == 'D':
        models = [
                MODEL1_D,
                MODEL2_D,
                MODEL3_D
            ]
    else:
        models = [
            MODEL1_G,
            MODEL2_G,
            MODEL3_G,
            MODEL1_G, # Workaround
            MODEL2_G,
            MODEL3_G
        ]

    agents = []
    for _, model_path in enumerate(models):
        agents.append(load_model(model_path))

    if gametype == 'D':
        span = 4
        num_hands = 200
        if is_hand:
            min_estimates = np.array([-172, -102, -52, -22, -12, -2, 8, 18, 28, 38, 48, 58, 62, 66, 70, 74, 78, 82, 86, 90, 94])
            possible_rewards = [-190, -170, -150, 80, 90, 100]
        else:
            min_estimates = np.array([-142, -102, -52, -22, -12, -2, 8, 18, 28, 38, 48, 58, 62, 66, 70, 74, 78, 82, 86])
            possible_rewards = [-170, -150, -130, 70, 80, 90]
    else:
        span = 8
        num_hands = 200
        if is_hand:
            min_estimates = np.array([-264, -104, -54, -24, -9, 6, 21, 36, 51, 66, 81, 96, 106, 116, 126, 136, 146, 156, 161])
            possible_rewards = [-330, -282, -234, 122, 146, 170]
        else:
            min_estimates = np.array([-204, -104, -54, -24, -9, 6, 21, 36, 51, 66, 81, 96, 106, 116, 126, 136, 146])
            possible_rewards = [-282, -234, -186, 98, 122, 146]

    value_distributions = np.zeros((len(min_estimates), num_hands, 6))
    actual_values = []

    for min_est_ind, min_est in enumerate(min_estimates):
        print(f'Getting distributions for {min_est + span/2}...')
        
        actual_values_list = []
        hand_ind = 0
        while hand_ind < num_hands:
            print(f'Hand Nummer {hand_ind+1}...')

            num_fails = 0
            while True:
                player_id = 2
                while player_id != 0:
                    env = SkatEnv(seed=None, gametype=gametype)

                    env.set_agents(agents)

                    raw_state, player_id = env.game.init_game()

                #print(env.game.players[0].current_hand)
                #print(env.game.state['skat'])

                bids_cpy = copy.deepcopy(env.game.round.dealer.bids)
                bid_jacks_cpy = copy.deepcopy(env.game.round.dealer.bid_jacks)

                bidder = Bidder(env, raw_state, pos='0')
                hand_estimate = bidder.get_blind_hand_values_for_game(gametype) # irreführender Name, da hier mit Skat und nicht blind

                if hand_estimate < min_est or hand_estimate > min_est + span:
                    continue
                else:
                    print(hand_estimate)
                    break

            env_cpy = copy.deepcopy(env)

            results = {'Eigenschwarz': [0], 'Eigenschneider': [0], 'Verloren': [0], 'Gewonnen': [0], 'Schneider': [0], 'Schwarz': [0]}
            trajectories, rewards = env.run(state=raw_state, player_id=player_id)

            results['Eigenschwarz'].append(((rewards[0] == possible_rewards[0])))
            results['Eigenschneider'].append(((rewards[0] == possible_rewards[1])))
            results['Verloren'].append(((rewards[0] == possible_rewards[2])))
            results['Gewonnen'].append(((rewards[0] == possible_rewards[3])))
            results['Schneider'].append(((rewards[0] == possible_rewards[4])))
            results['Schwarz'].append(((rewards[0] == possible_rewards[5])))
          
            actual_values_list.append(hand_estimate)

            value_distributions[min_est_ind, hand_ind, 0] = results['Eigenschwarz'][-1]
            value_distributions[min_est_ind, hand_ind, 1] = results['Eigenschneider'][-1]
            value_distributions[min_est_ind, hand_ind, 2] = results['Verloren'][-1]
            value_distributions[min_est_ind, hand_ind, 3] = results['Gewonnen'][-1]
            value_distributions[min_est_ind, hand_ind, 4] = results['Schneider'][-1]
            value_distributions[min_est_ind, hand_ind, 5] = results['Schwarz'][-1]

            hand_ind += 1

        actual_values.append(np.mean(actual_values_list))

        #print(rewards)

    #plt.figure()
    #plt.plot(running_value_means)
    #plt.legend(['Eigenschwarz', 'Eigenschneider', 'Verloren', 'Gewonnen', 'Schneider', 'Schwarz'])
    #plt.show()

    if is_hand:
        np.save(f'bidding/data/new_values_{gametype}H.npy', actual_values)
        np.save(f'bidding/data/new_outcome_distributions_{gametype}H.npy', value_distributions)
    else:
        np.save(f'bidding/data/new_values_{gametype}.npy', actual_values)
        np.save(f'bidding/data/new_outcome_distributions_{gametype}.npy', value_distributions)

    print('Ende')