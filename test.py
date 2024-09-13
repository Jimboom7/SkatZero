import statistics

from skatzero.env.skat import SkatEnv
from skatzero.evaluation.simulation import load_model
from skatzero.test.testcases import *
from skatzero.test.utils import run_testcase

def run_testsuite(model, version):
    MODEL1 = "models/checkpoints/" + model + "/0_" + str(version) + ".pth"
    MODEL2 = "models/checkpoints/" + model + "/1_" + str(version) + ".pth"
    MODEL3 = "models/checkpoints/" + model + "/2_" + str(version) + ".pth"

    models = [
            MODEL1,
            MODEL2,
            MODEL3
        ]

    agents = []
    for _, model_path in enumerate(models):
        agents.append(load_model(model_path))

    env = SkatEnv(gametype=model[-1])

    env.set_agents(agents)

    raw_state, _ = env.game.init_game()

    if model == 'skat_D' or model == 'skat_lstm_D':
        # testcases = [case1_bonus]
        testcases = [case1_easy, case2_easy, case3_easy, case4_easy, case5_easy, case6_easy, case7_easy, case8_easy, case9_easy, case10_easy,
                   case2_medium, case3_medium, case4_medium, case5_medium, case6_medium, case7_medium, case8_medium, case9_medium, case10_medium,
                   case11_medium, case12_medium, case13_medium, case14_medium, case15_medium, case16_medium, case17_medium, case18_medium, case19_medium, case20_medium,
                   case21_medium, case22_medium, case23_medium, case24_medium, case25_medium, case26_medium, case27_medium, case28_medium, case29_medium, case30_medium, case31_medium,
                   case1_hard, case2_hard, case3_hard, case4_hard, case5_hard, case6_hard, case7_hard, case8_hard, case9_hard, case10_hard]
    elif model == 'skat_G' or model == 'skat_lstm_G':
        testcases = [case1_easy_grand, case2_easy_grand, case3_easy_grand, case1_medium_grand, case2_medium_grand, case3_medium_grand, case1_hard_grand, case2_hard_grand, case1_euroskat_grand]
    elif model == 'skat_N' or model == 'skat_lstm_N':
        testcases = [case1_null]

    w_score = 0
    c_score = 0
    correct = 0
    correct2 = 0
    results = []
    for testcase in testcases:
        w_diff, c_diff, pos = run_testcase(testcase, raw_state, env, agents)
        w_score += w_diff
        c_score += c_diff
        if w_diff == 0:
            if pos == 0:
                correct += 1
            else:
                correct2 += 1
        if w_diff == 0:
            results.append(c_diff)
        else:
            results.append(w_diff)
    if correct + correct2 == 0:
        correct = 0.0001
    if correct + correct2 == len(testcases):
        correct -= 0.0001
    print("Overall")
    print("Score for Failed: " + str(w_score / (len(testcases) - correct)))
    print("Score for Passed: " + str(c_score / correct))
    print("Correct: " + str(correct) + " + " + str(correct2) + "/" + str(len(testcases)))

    with open("testresults/test_results.csv", "a", encoding='utf-8') as logfile:
        logfile.write(str(model) + "," + str(version) + "," + str(correct) + "," + str(correct2) + "," + str((c_score + w_score) / len(testcases)) + "\n")
        # Plot: https://list2chart.com/csv-to-chart/
    return correct, ((c_score + w_score) / len(testcases)), results

def get_averages(model, version):
    moving_average_c = []
    moving_average_d = []
    detailed_list = []
    for i in range(10, version + 10, 10):
        if len(moving_average_c) >= 10:
            moving_average_c = moving_average_c[1:]
            moving_average_d = moving_average_d[1:]
        correct, diff, results = run_testsuite(model, i)
        moving_average_c.append(correct)
        moving_average_d.append(diff)
        detailed_list.append(results)
        with open("testresults/test_results_avg.csv", "a", encoding='utf-8') as logfile:
            logfile.write(str(model) + "," + str(i) + "," + str(statistics.fmean(moving_average_c)) + "," + str(statistics.fmean(moving_average_d)) + "\n")
    for i in range(50):
        res = ""
        for j, x in enumerate(detailed_list):
            res += str((j + 1) * 10) + "," + str(x[i]) + "\n"
        with open("testresults/testcases/test_" + str(i + 1) + ".csv", "a+", encoding='utf-8') as logfile:
            logfile.write(res)

if __name__ == '__main__':
    MODEL = "skat_lstm_D"
    FRAMES = 16030
    # MODEL = "skat_lstm_G"
    # FRAMES = 13070
    #MODEL = "skat_N"
    #FRAMES = 1600

    # run_testsuite(MODEL, FRAMES)

    for i in range(16010, FRAMES + 10, 10):
        try:
            run_testsuite(MODEL, i)
        except:
            pass


    #get_averages(MODEL, FRAMES)
