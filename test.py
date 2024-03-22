from skatzero.env.skat import SkatEnv
from skatzero.evaluation.simulation import load_model
from skatzero.test.testcases import *
from skatzero.test.utils import run_testcase

if __name__ == '__main__':

    CHECKPOINT_DIR = "checkpoints/skat_30_final"
    FRAMES = "700"

    MODEL1 = CHECKPOINT_DIR + "/0_" + FRAMES + ".pth"
    MODEL2 = CHECKPOINT_DIR + "/1_" + FRAMES + ".pth"
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

    testcases = [case1, case2, case3, case4, case5, case6, case7, case8, case9, case10,
                 case11, case12, case13, case14, case15, case16, case17]

    w_score = 0
    c_score = 0
    correct = 0
    for testcase in testcases:
        w_diff, c_diff = run_testcase(testcase, raw_state, env, agents)
        w_score += w_diff
        c_score += c_diff
        if w_diff == 0:
            correct += 1
    print("Overall")
    print("Score for Failed: " + str(w_score / (len(testcases) - correct)))
    print("Score for Passed: " + str(c_score / correct))
    print("Correct: " + str(correct) + "/" + str(len(testcases)))
