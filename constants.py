from PIL import Image, ImageDraw, ImageFont


# Display related parameters
MENU_GAP = 200  # The gap of the top menu that shows turn and scores in the display.
SIZE = 1800 # The display size.
SPACING = (SIZE)//6 # The space between the lines on the display.
IS_VISUALIZER_ON = False # Whether to display the game or not.
WAIT_TIME = 0   # The wait time between moves.
SHOW_EVERY = 1  # The frequency of displaying the game.

# Model training related parameters
SCORE_REWARD = 1  # The score reward for each completed SOS sequence.
REWARD_INCREASE_RATE = 0.5  # The rate at which the Q-value increases based on the reward.
REWARD_DECREASE_RATE = 0.2 # The rate at which the Q-value decreases based on the reward.
LR = 0.01   # The learning rate for the Q-learning algorithm.
UPDATE_TARGET_EVERY = 5 # The frequency at which the model is updated.
EPSILON = 1  # The probability of making a random move.
EPSILON_DECAY = 0.99999 # The rate at which the epsilon value decreases.
MIN_EPSILON = 0.01  # The minimum epsilon value.

# Model saving related parameters
IS_TEST = True  # Whether it is a test run (the model will not be saved).
MODEL_NAME = "B"    # The name for saving the trained model.
LOAD_MODEL = False   # Whether to load a pre-trained model or create a new one.
MODEL_PATH = "models/A 530k.model" #   The path to the pre-trained model to load.
AGGREGATE_STATS_EVERY = 10000   # The frequency at which the model's statistics are saved.
EPISODES = 2_000_000    # The total number of episodes to be played during training.




ACTION_LIST = [(0,0),(0,1),(0,2),(0,3),(0,4),(0,5), # List of actions that can be played
               (1,0),(1,1),(1,2),(1,3),(1,4),(1,5),
               (2,0),(2,1),(2,2),(2,3),(2,4),(2,5),
               (3,0),(3,1),(3,2),(3,3),(3,4),(3,5),
               (4,0),(4,1),(4,2),(4,3),(4,4),(4,5),
               (5,0),(5,1),(5,2),(5,3),(5,4),(5,5)]

pieces= {"":"", "S":"S", "O":"O"}   # Dictionary of pieces in the game
for piece in pieces:    # Creating images of pieces
    image = Image.new("RGBA", (SPACING, SPACING))   # Creating an image
    drawer = ImageDraw.Draw(image, 'RGBA')  # Creating a drawer to draw pieces on the image
    fnt = ImageFont.truetype("arial.ttf", 250)  # Setting font

    if pieces[piece] == "S":
        drawer.text((-10,-37), "S", font=fnt)   # Drawing S to image, if piece is S
    elif pieces[piece] == "O":
        drawer.text((-10,-37), "O", font=fnt)   # Drawing O to image, if piece is O

    pieces[piece] = image   # Assigning the created image to the current piece in the pieces dictionary