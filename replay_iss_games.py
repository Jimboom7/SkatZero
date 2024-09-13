"""
Read a iss.log file.
Deals the exact same cards and lets AI agents play them.
"""
from iss.SkatMatch import SkatMatch
from skatzero.evaluation.simulation import load_model, set_dealer_data, set_seed
from skatzero.evaluation.eval_env import EvalEnv

def get_reward(score, is_hand, base_value):
    if score == 120:
        return ((4 + is_hand) * base_value) + 50
    elif score >= 90:
        return ((3 + is_hand) * base_value) + 50
    elif score > 60:
        return ((2 + is_hand) * base_value) + 50
    elif score == 0:
        return (((-4 - is_hand) * 2) * base_value) - 50 - 40
    elif score <= 30:
        return (((-3 - is_hand) * 2) * base_value) - 50 - 40
    elif score <= 60:
        return (((-2 - is_hand) * 2) * base_value) - 50 - 40

if __name__ == '__main__':

    seed = 42
    set_seed(seed)

    gametype = 'D'
    name = 'Hubert47'

    model_d = '14690'
    model_g = '11450'
    # model_d = '15200'
    # model_g = '12180'
    # model_d = '15200'
    # model_g = '12560'

    with open('C:/Users/janvo/Desktop/Skat/ISS-Bot/logs/log_' + model_d + '_' + model_g + '.txt', encoding='utf-8') as fRaw:
    # with open('C:/Users/janvo/Desktop/Skat/ISS-Bot/log.txt', encoding='utf-8') as fRaw:

        line = fRaw.readline()

        dealers = []

        points = 0
        pos = [0,0,0]
        pos2 = [0,0,0]

        while line:
            try:
                match = SkatMatch(line)
                if not match.eingepasst and (gametype == match.gameType[0] or (gametype == 'D' and match.gameType[0] in ['H', 'S', 'C'])):
                    if match.playerNames[match.alleinspielerInd] == name or match.playerNames[match.alleinspielerInd] == name + ':2':
                        pos[match.alleinspielerInd] += 1
                        if match.stichPoints > 60:
                            pos2[match.alleinspielerInd] += 1
                        dealer = set_dealer_data(match, gametype)
                        dealers.append(dealer)
                        points += get_reward(match.stichPoints, match.is_hand, 10 if gametype == 'D' else 24)
                        #print(line)
                        #print(get_reward(match.stichPoints, match.is_hand, 10))
            except:
                pass
            line = fRaw.readline()
        print("Anzahl Spiele: " + str(len(dealers)))
        print(points / len(dealers))
    
    print(pos)
    print(pos2)

    for i in range(16010, 16040, 10):
        env = EvalEnv(seed=seed, gametype=gametype, lstm=[True, True, True], dealers=dealers)

        if gametype == 'D':
            agent_0 = load_model('models/checkpoints/skat_lstm_D/0_' + model_d + '.pth')
            agent_1 = load_model('models/checkpoints/skat_lstm_D/1_' + str(i) + '.pth')
            agent_2 = load_model('models/checkpoints/skat_lstm_D/2_' + str(i) + '.pth')
        else:
            agent_0 = load_model('models/checkpoints/skat_lstm_G/0_' + model_g + '.pth')
            agent_1 = load_model('models/checkpoints/skat_lstm_G/1_' + str(i) + '.pth')
            agent_2 = load_model('models/checkpoints/skat_lstm_G/2_' + str(i) + '.pth')

        env.set_agents([
            agent_0,
            agent_1,
            agent_2,
        ])

        points = 0
        for d in dealers:
            trajectories, rewards = env.run(is_training=False, verbose=0)
            points += rewards[0]
            #print(rewards[0])
        print("Modell: " + str(i))
        print(points / len(dealers))
