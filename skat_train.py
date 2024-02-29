import os

import rlcard
from rlcard.agents.dmc_agent import DMCTrainer

def train():

    # Make the environment
    env = rlcard.make('skat')

    # Initialize the DMC trainer
    trainer = DMCTrainer(
        env,
        cuda="", # Empty = cpu, 0 = GPU
        xpid='skat_2',
        savedir='experiments/skat',
        save_interval=30, # save model every 30 minutes
        num_actors=5,
        training_device="cpu",
        load_model=False,
        total_frames=10000000 # 1 million takes around 3 minutes
    )

    # Train DMC Agents
    trainer.start()

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    train()
