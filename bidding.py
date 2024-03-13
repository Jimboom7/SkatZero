from skatzero.evaluation.utils import format_card
from skatzero.evaluation.simulation import get_bidding_data

if __name__ == '__main__':
    CHECKPOINT_DIR = "checkpoints/skat_17_new_baseline"
    FRAMES = "10"
    SOLOPLAYER = CHECKPOINT_DIR + "/soloplayer_" + FRAMES + ".pth"
    OPPONENT_LEFT = "random"
    OPPONENT_RIGHT = "random"

    values, actions = get_bidding_data(SOLOPLAYER, True)

    for i, a in enumerate(actions):
        print(format_card(a) + ": " + str(values[i]))
