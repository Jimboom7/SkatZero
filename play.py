from skatzero.evaluation.simulation import load_model
from skatzero.agents.human_agent import HumanAgent
from skatzero.env.skat import SkatEnv

if __name__ == '__main__':
    env = SkatEnv()

    MODEL1 = 'checkpoints/skat_20_flexible_suits/0_40.pth'
    MODEL2 = 'checkpoints/skat_20_flexible_suits/2_40.pth'

    human_agent = HumanAgent(env.num_actions)
    dcm_agent_0 = load_model(MODEL1)
    dcm_agent_2 = load_model(MODEL2)
    env.set_agents([
        dcm_agent_0,
        human_agent,
        dcm_agent_2,
    ])

    print(">> Skat pre-trained model")

    while True:
        print(">> Start a new game")

        trajectories, rewards = env.run(is_training=False)

        print('===============     Result     ===============')
        print("Rewards:")
        print(rewards)

        input("Press any key to continue...")
