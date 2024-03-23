from skatzero.env.skat import SkatEnv
from skatzero.evaluation.simulation import load_model
from skatzero.test.testcases import *
from skatzero.test.utils import run_testcase

def run_testsuite(model, version):
    MODEL1 = "checkpoints/" + model + "/0_" + str(version) + ".pth"
    MODEL2 = "checkpoints/" + model + "/1_" + str(version) + ".pth"
    MODEL3 = "checkpoints/" + model + "/2_" + str(version) + ".pth"

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
                 case11, case12, case13, case14, case15, case16, case17, case18, case19, case20]

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

    with open("test_results.csv", "a", encoding='utf-8') as logfile:
        logfile.write(str(model) + "," + str(version) + "," + str(correct) + "," + str((c_score / correct) - w_score / (len(testcases) - correct)) + "\n")

if __name__ == '__main__':
    MODEL = "skat_30_final"
    FRAMES = 970

    run_testsuite(MODEL, FRAMES)

    #for i in range(10, FRAMES + 10, 10):
    #    run_testsuite(MODEL, i)
