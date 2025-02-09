# SkatZero

SkatZero is a reinforcement learning AI for the German card game [Skat](https://www.skatinsel.academy/en/how-to-skat/rules). In this 3-player card game, one of the players is up against two cooperating opponents, which makes this incomplete information game extremely challenging for AIs. Conventional AI algorithms exist (e.g., Kermit), but are not on the level of expert players yet.  

This project uses Deep Monte Carlo reinforcement learning without prior knowledge of the game rules. That means it plays millions of games against itself, first with random moves and over time with more strategic gameplay. The results are promising. While SkatZero is still not quite on the level of top-level players, it beats conventional AIs by quite a margin. The time to make a move is also extremely low (just a few milliseconds) due to the nature of neural networks. The following image shows the ranking on the International Skat Server after playing thousands of games against other AIs (Kermit).  

[IMAGE]

## Architecture

### Network Architecture

The architecture of the project is based on [DouZero](https://github.com/kwai/DouZero) for the chinese card game Dou Dizhu. Major changes were made for the features, card encoding and the game logic, while the network architecture is mostly the same (6-layer MLP, with the action and state of the game as input, as well as the historical moves preprocessed by an LSTM network). There are 3 models for each game type (Suit Game, Grand, Null), meaning a total of 9 models need to be trained. Details on the network architecture can be found in the [DouZero Paper](https://arxiv.org/pdf/2106.06135).  

#### Features
The features differ for the solo and opposing players, as well as game type. Everything is encoded as a one hot matrix.  
In general the features are the following:  
**Action**:
Card
**Game State**:
Current Hand
Opponent Hand
Card 1 in trick
Card 2 in trick
Cards in skat
Missing Cards of other players
Cards Played by other players
Solo Player Points
Opponent Points
Information about bidding
Is Blind Hand Game
**Game History**:
All cards and the player who played them in chronological order

### Bidding Architecture

Bidding was not the focus of the AI, but it was necessary to play games in the ISS against other AIs and evaluate the performance. Due to the complexity of the bidding process, it was not included in the actual AI itself, meaning the AI learns only which cards to discard in the actual game. A conventional algorithm was written for the bidding process, utilizing the expected win rate that the AI outputs for the first discard. Since the inference time is very low, it is feasible to simulate all possible hands (for all Skat pickups and putting down of 2 cards) in a reasonable time. This can be done for all 3 game types and be used to calculate how high to bid.  
The bidding algorithm is far from perfect, since it does not really take into account other player bids. An idea for the future would be to integrate bidding into the AI, or train another AI only for bidding (like it was done in [AlphaDou](https://arxiv.org/abs/2407.10279)).

## Training

Training was done on a regular PC with one RTX 4070 Ti and an Intel Core i7-12700F. Only the learning process was run on the GPU, the actors that played the games were run on 16 cores (processes) on the CPU. The total training time was 500 hours each for the suit-game model and grand-game model, each of those models played around 1.5 billion games in that time. The null-game model took less time to train, since the gameplay is simpler.

## Dependencies

- Pytorch

## Usage

### Training

To train the models, run the following command:
```sh
python train.py
```
Most of the parameters in the file can usually be kept at the default. Only the number of actors should be changed depending on your hardware.

### Evaluation

To evaluate the trained models, run the following command:
```sh
python evaluate.py
```
This will let a specific version of a model play multiple games against another model, to check how much the performance increased.

### Play

To play against the model locally (without bidding), run the following command:
```sh
python play.py
```

### Tests

To start the tests, run the following command:
```sh
python test.py
```
There are testcases for each game mode ranging from simple to challenging puzzles.

## License
This project is licensed under the MIT License - see the LICENSE file for details.