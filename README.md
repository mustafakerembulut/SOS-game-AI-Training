# SOS-game-AI-Training

The SOS Game AI Training project aims to develop an AI model capable of playing the SOS game. The game is played on a 6x6 grid, where players aim to score more points than their opponent by creating SOS sequences. The project includes the implementation of a Q-learning algorithm to train the AI model and improve its gameplay strategy.

## Prerequisites

You can install the required Python libraries by running:<br/>
`pip install -r requirements.txt`

## Getting Started

1. Clone the repository.
2. Navigate to the project directory.

## Adjustable Parameters

To customize the behavior of the SOS Game AI Training project, you can modify the following parameters in `constants.py`:

#### Display Related Parameters

- `MENU_GAP`: The gap of the top menu that shows turn and scores in the display.
- `SIZE`: The display size.
- `SPACING`: The space between the lines on the display.
- `IS_VISUALIZER_ON`: Whether to display the game or not.
- `WAIT_TIME`: The wait time between moves.
- `SHOW_EVERY`: The frequency of displaying the game.

#### Model Training Related Parameters

- `SCORE_REWARD`: The score reward for each completed SOS sequence.
- `REWARD_INCREASE_RATE`: The rate at which the Q-value increases based on the reward.
- `REWARD_DECREASE_RATE`: The rate at which the Q-value decreases based on the reward.
- `LR`: The learning rate for the Q-learning algorithm.
- `UPDATE_TARGET_EVERY`: The frequency at which the model is updated.
- `EPSILON`: The probability of making a random move.
- `EPSILON_DECAY`: The rate at which the epsilon value decreases.
- `MIN_EPSILON`: The minimum epsilon value.

#### Model Saving Related Parameters

- `IS_TEST`: Whether it is a test run (the model will not be saved).
- `MODEL_NAME`: The name for saving the trained model.
- `LOAD_MODEL`: Whether to load a pre-trained model or create a new one.
- `MODEL_PATH`: The path to the pre-trained model to load.
- `AGGREGATE_STATS_EVERY`: The frequency at which the model's statistics are saved.
- `EPISODES`: The total number of episodes to be played during training.

Also you can adjust the model's layer, activation function's of layers, optimizer and loss function in:`sos_agent.py`

## Training the AI Model

To start training the AI model, adjust the parameters in `constants.py` as desired. After making the adjustments, run: `sos_main.py`

This will initiate the training process, where the AI model plays against itself and learns to make intelligent moves using the Q-learning algorithm.

## Viewing Training Logs with TensorBoard

During the training process, logs are saved in "logs" directory with model name.
To view the training logs using TensorBoard,
1. Open a terminal or command prompt and navigate to the project directory.
2. Run the following command to start TensorBoard: `tensorboard --logdir logs`
  - This will start TensorBoard and load the logs from the "logs" directory.
3. Open a web browser and visit the following URL to access the TensorBoard dashboard: `http://localhost:6006/`
  - Also you can try Ctrl+clicking the URL, it will automaticly open url on your web browser

## Playing Against the Trained AI Model

To play against the trained AI model,
- Adjust the `model_path` and `wait_time` in the `play_vs_ai.py`.
- After making the adjustments, run: `play_vs_ai.py`

## Game Rules

1. The SOS game is played on a 6x6 grid.
2. Players take turns making moves.
3. Each move consists of placing either an "S" or an "O" on the grid.
4. Players aim to create SOS sequences, where "S" is followed by "O" and then followed by another "S", either horizontally, vertically, or diagonally.
5. Players earn one point for each completed SOS sequence.
6. The game continues until the grid is filled.
7. The player with the highest score at the end of the game wins.
