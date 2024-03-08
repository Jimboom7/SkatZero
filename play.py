''' Play against the AI
'''
from skatzero.evaluation.simulation import sample

if __name__ == '__main__':
    CHECKPOINT_DIR = "checkpoints/skat_2_mod3_history"
    FRAMES = "150028800"

    SOLOPLAYER = CHECKPOINT_DIR + "/soloplayer_" + FRAMES + ".pth"
    OPPONENT_LEFT = 'rulebased' #CHECKPOINT_DIR + "/opponent_left_" + FRAMES + ".pth"
    OPPONENT_RIGHT = "human"

    game_infosets = sample('eval_data.pkl', SOLOPLAYER, OPPONENT_LEFT, OPPONENT_RIGHT, True)

    if game_infosets[:-1].score['soloplayer'] > 60:
        print("Soloplayer won!")
