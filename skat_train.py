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
        xpid='skat_0',
        savedir='experiments/skat',
        save_interval=10, # save model every 10 minutes
        num_actors=6, # more than 6 doesnt improve performance on cpu
        training_device="0",
        load_model=True,
        eval=True,
        total_frames=10000000 # 1 million takes around 3 minutes
    )

    # Train DMC Agents
    trainer.start()

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    train()
