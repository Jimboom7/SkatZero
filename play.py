from skatzero.agents.rule_based_agent import RuleBasedAgent
from skatzero.evaluation.simulation import load_model, set_seed
from skatzero.agents.human_agent import HumanAgent
from skatzero.env.skat import SkatEnv

if __name__ == '__main__':

    seed = 48
    set_seed(seed)

    env = SkatEnv(seed=seed, gametype='D')

    #agent_0 = load_model('models/latest/' + env.game.gametype + '_0.pth')
    agent_0 = HumanAgent(env.num_actions)
    #agent_2 = RuleBasedAgent(env.num_actions)
    agent_1 = load_model('models/latest/' + env.game.gametype + '_1.pth')
    agent_2 = load_model('models/latest/' + env.game.gametype + '_2.pth')

    env.set_agents([
        agent_0,
        agent_1,
        agent_2,
    ])

    print(">> Skat pre-trained model")

    while True:
        print(">> Start a new game")

        trajectories, rewards = env.run(is_training=False, verbose=1)

        print('===============     Result     ===============')
        print("Rewards:")
        print(rewards)

        input("Press any key to continue...")
