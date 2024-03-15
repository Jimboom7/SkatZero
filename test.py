from skatzero.env.skat import SkatEnv
from skatzero.evaluation.utils import format_card
from skatzero.evaluation.simulation import get_bidding_data, load_model

if __name__ == '__main__':

    CHECKPOINT_DIR = "checkpoints/skat_22_smooth_rewards"
    FRAMES = "150"

    MODEL1 = CHECKPOINT_DIR + "/0_" + FRAMES + ".pth"
    MODEL2 = CHECKPOINT_DIR + "/0_" + FRAMES + ".pth"
    MODEL3 = CHECKPOINT_DIR + "/0_" + FRAMES + ".pth"

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




    state = env.extract_state(raw_state)

    #print(state)

    _, info = agents[0].eval_step(state)

    print(info)
