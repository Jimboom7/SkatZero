import os

import rlcard
from rlcard.agents.dmc_agent import DMCTrainer

def train():

    # Make the environment
    env = rlcard.make('doudizhu')

    # Initialize the DMC trainer
    trainer = DMCTrainer(
        env,
        cuda="",
        xpid='doudizhu',
        savedir='experiments/doudizhu',
        save_interval=30,
        num_actor_devices=1,
        num_actors=5,
        training_device="0",
        total_frames=100000
    )

    # Train DMC Agents
    trainer.start()

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    train()