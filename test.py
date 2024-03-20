from skatzero.env.skat import SkatEnv
from skatzero.evaluation.utils import format_card
from skatzero.evaluation.simulation import get_bidding_data, load_model

def case1(raw_state):
    raw_state['trace'] = [(1, "S7"), (2, "SQ"), (0, "SA")]
    raw_state['played_cards'] = [["SA"],["S7"],["SQ"]]
    raw_state['self'] = 0
    raw_state['current_hand'] = ["SJ", "HJ", "DJ", "DK", "D9", "D7", "HA", "HK", "H8"]
    raw_state['others_hand'] = ["CJ", "D8", "DQ", "DT", "DA", "H7", "H9", "HQ", "HT", "S8", "SK", "ST", "C7", "C8", "C9", "CK", "CT", "CA"]
    raw_state['points'] = [0, 0]
    raw_state['actions'] = ["SJ", "HJ", "DJ", "DK", "D9", "D7", "HA", "HK", "H8"]
    raw_state['trick'] = []
    raw_state['blind_hand'] = False
    raw_state['skat'] = ['CQ', 'S9']
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 0, 0]
    return raw_state

def case2(raw_state):
    raw_state['trace'] = [(1, "SK")]
    raw_state['played_cards'] = [[],["SK"],[]]
    raw_state['self'] = 2
    raw_state['current_hand'] = ["DJ", "HJ", "S7", "S8", "S9", "ST", "HQ", "HK", "CA", "C8"]
    raw_state['others_hand'] = ["SJ", "D7", "D8", "D9", "DQ", "DK", "DT", "DA", "H7", "H8", "H9", "HT", "HA", "SQ", "CJ", "C7", "C9", "CQ", "CT", 'CK', 'SA']
    raw_state['points'] = [0, 0]
    raw_state['actions'] = ["S7", "S8", "S9", "ST"]
    raw_state['trick'] = [(1, "SK")]
    raw_state['blind_hand'] = False
    raw_state['skat'] = []
    raw_state['bids'] = [{'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 1, 'H': 0, 'S': 0, 'C': 0, 'N': 0},
                    {'D': 0, 'H': 0, 'S': 0, 'C': 0, 'N': 0}]
    raw_state['bid_jacks'] = [0, 2, 0]
    return raw_state

if __name__ == '__main__':

    CHECKPOINT_DIR = "checkpoints/skat_27_final"
    FRAMES = "550"

    MODEL1 = CHECKPOINT_DIR + "/2_" + FRAMES + ".pth"
    MODEL2 = CHECKPOINT_DIR + "/2_" + FRAMES + ".pth"
    MODEL3 = CHECKPOINT_DIR + "/2_" + FRAMES + ".pth"

    models = [
            MODEL1,
            MODEL2,
            MODEL3
        ]

    agents = []
    for _, model_path in enumerate(models):
        agents.append(load_model(model_path))

    env = SkatEnv()

    env.set_agents(agents)

    raw_state, player_id = env.game.init_game(blind_hand=False)

    # https://www.youtube.com/watch?v=rc0C9xftSfs
    #raw_state = case1(raw_state)

    #Testcase for Javascript Comparison
    raw_state = case2(raw_state)

    state = env.extract_state(raw_state)

    print(state)
    with open('obs.txt', 'a') as the_file:
        for obs in state['obs']:
            the_file.write('    ' + str(obs) + ',\n')

    _, info = agents[1].eval_step(state)

    print(info)
