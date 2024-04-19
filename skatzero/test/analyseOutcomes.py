import matplotlib.pyplot as plt
import numpy as np

import copy
import random
import sys
sys.path.append('D:\Git\skatzero')
from skatzero.env.skat import SkatEnv
from skatzero.evaluation.utils import format_card
from skatzero.evaluation.simulation import get_bidding_data, prepare_env, load_model
from skatzero.evaluation.bidder import Bidder

if __name__ == '__main__':

    MODEL1 = "model/0.pth"
    MODEL2 = "model/1.pth"
    MODEL3 = "model/2.pth"

    models = [
            MODEL1,
            MODEL2,
            MODEL3
        ]

    agents = []
    for _, model_path in enumerate(models):
        agents.append(load_model(model_path))


    span = 4
    min_estimates = np.concatenate(([-147, -102, -52, -22], np.arange(-12, 68, 10), np.arange(62, 90, 4)))
    #min_est = -0.5
    num_hands = 100 # 40
    #value_distributions = np.zeros((1, num_hands, 6))
    #running_value_means = np.zeros((num_hands, 6))
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
                    env = SkatEnv(blind_hand_chance = 0.0, seed=None)

                    env.set_agents(agents)

                    raw_state, player_id = env.game.init_game(blind_hand=False)

                #print(env.game.players[0].current_hand)
                #print(env.game.state['skat'])

                bids_cpy = copy.deepcopy(env.game.round.dealer.bids)
                bid_jacks_cpy = copy.deepcopy(env.game.round.dealer.bid_jacks)

                bidder = Bidder(env, raw_state, pos="0")
                hand_estimates = bidder.get_blind_hand_values()

                if hand_estimates[3] < min_est or hand_estimates[3] > min_est + span:
                    continue
                else:
                    print(hand_estimates)
                    break

            env_cpy = copy.deepcopy(env)

            results = {'Eigenschwarz': [0], 'Eigenschneider': [0], 'Verloren': [0], 'Gewonnen': [0], 'Schneider': [0], 'Schwarz': [0]}
            num_distributions = 10 #20
            distribution_count = 0
            is_stuck = False
            while distribution_count < num_distributions:
                env = copy.deepcopy(env_cpy)
                other_cards = env.game.players[1].current_hand + env.game.players[2].current_hand
                random.shuffle(other_cards)
                env.game.players[1].current_hand = other_cards[:10]
                env.game.players[2].current_hand = other_cards[10:]
                env.game.round.dealer.reset_bids()
                env.game.round.dealer.set_bids(env.game.players)

                if env.game.round.dealer.bids != bids_cpy or env.game.round.dealer.bid_jacks != bid_jacks_cpy: #bleibt manchmal hängen
                    num_fails += 1
                    if num_fails == 300: #400
                        is_stuck = True
                        break
                    continue

                distribution_count += 1
                #print(env.game.round.dealer.bids)
                #print(env.game.players[0].current_hand)
                #print(env.game.players[1].current_hand)
                #print(env.game.players[2].current_hand)
                trajectories, rewards = env.run(state=raw_state, player_id=player_id)
                #print(rewards)

                #if rewards[0] == -170:
                #    results['Eigenschwarz'] += 1
                #elif rewards[0] == -150:
                #    results['Eigenschneider'] += 1
                #elif rewards[0] == -130:
                #    results['Verloren'] += 1
                #elif rewards[0] == 70:
                #    results['Gewonnen'] += 1
                #elif rewards[0] == 80:
                #    results['Schneider'] += 1
                #elif rewards[0] == 90:
                #    results['Schwarz'] += 1

                results['Eigenschwarz'].append(((rewards[0] == -170) + results['Eigenschwarz'][-1]*(distribution_count-1))/distribution_count)
                results['Eigenschneider'].append(((rewards[0] == -150) + results['Eigenschneider'][-1]*(distribution_count-1))/distribution_count)
                results['Verloren'].append(((rewards[0] == -130) + results['Verloren'][-1]*(distribution_count-1))/distribution_count)
                results['Gewonnen'].append(((rewards[0] == 70) + results['Gewonnen'][-1]*(distribution_count-1))/distribution_count)
                results['Schneider'].append(((rewards[0] == 80) + results['Schneider'][-1]*(distribution_count-1))/distribution_count)
                results['Schwarz'].append(((rewards[0] == 90) + results['Schwarz'][-1]*(distribution_count-1))/distribution_count)


                #if distribution_count % 100 == 0:
                #    print(distribution_count)

            #print(results)

            #plt.figure()
            #plt.plot(results['Eigenschwarz'])
            #plt.plot(results['Eigenschneider'])
            #plt.plot(results['Verloren'])
            #plt.plot(results['Gewonnen'])
            #plt.plot(results['Schneider'])
            #plt.plot(results['Schwarz'])
            #plt.legend(['Eigenschwarz', 'Eigenschneider', 'Verloren', 'Gewonnen', 'Schneider', 'Schwarz'])
            #plt.show()

            if is_stuck:
                #print('This hand was stuck...')
                continue

            true_mean_value = results['Eigenschwarz'][-1] * (-170) + results['Eigenschneider'][-1] * (-150) + results['Verloren'][-1] * (-130) + results['Gewonnen'][-1] * (70) + results['Schneider'][-1] * (80) + results['Schwarz'][-1] * (90)
            actual_values_list.append(hand_estimates[-1])
            #print(f'True mean value without smooth points is {true_mean_value}')
            #print(env.game.state['skat'])
                
            #hand_cards = bidder.get_hand_cards()
            #for card in hand_cards:
            #    print(f'{format_card(card)}')

            value_distributions[min_est_ind, hand_ind, 0] = results['Eigenschwarz'][-1]
            value_distributions[min_est_ind, hand_ind, 1] = results['Eigenschneider'][-1]
            value_distributions[min_est_ind, hand_ind, 2] = results['Verloren'][-1]
            value_distributions[min_est_ind, hand_ind, 3] = results['Gewonnen'][-1]
            value_distributions[min_est_ind, hand_ind, 4] = results['Schneider'][-1]
            value_distributions[min_est_ind, hand_ind, 5] = results['Schwarz'][-1]

            #running_value_means[hand_ind] = np.mean(value_distributions[0, :hand_ind+1], axis=0)

            hand_ind += 1

        actual_values.append(np.mean(actual_values_list))

        
        #print(rewards)

    #plt.figure()
    #plt.plot(running_value_means)
    #plt.legend(['Eigenschwarz', 'Eigenschneider', 'Verloren', 'Gewonnen', 'Schneider', 'Schwarz'])
    #plt.show()

    np.save('values.npy', actual_values)
    np.save('outcome_distributions.npy', value_distributions)

    print('Ende')