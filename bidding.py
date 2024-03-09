''' An sample of playing skat randomly. Good for checking the internal values of the game, observation data etc.
'''
from skatzero.evaluation.utils import format_card
from skatzero.evaluation.simulation import bidding

if __name__ == '__main__':
    CHECKPOINT_DIR = "checkpoints/skat_2_mod3_history"
    FRAMES = "200016000"
    SOLOPLAYER = CHECKPOINT_DIR + "/soloplayer_" + FRAMES + ".pth"
    #OPPONENT_LEFT = CHECKPOINT_DIR + "/opponent_left_" + FRAMES + ".pth"
    #OPPONENT_RIGHT = CHECKPOINT_DIR + "/opponent_right_" + FRAMES + ".pth"
    # SOLOPLAYER = "random"
    OPPONENT_LEFT = "random"
    OPPONENT_RIGHT = "random"

    values, actions = bidding('eval_data.pkl', SOLOPLAYER, OPPONENT_LEFT, OPPONENT_RIGHT, True)

    for i, a in enumerate(actions):
        print(format_card(a) + ": " + str(values[i]))
