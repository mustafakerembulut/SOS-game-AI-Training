import numpy as np
import random
import torch
from collections import deque
import time
from sos import SOSEnv
from visualizer_vs import Visualizer
from sos_agent import DDQN
import random

model_name = "A"
k = 530
model_path = f"models/{model_name}/{model_name} {k}k.model"
wait_time = 1


visualizer = Visualizer()
env = SOSEnv()
visualizer.env = env
s = "S"
o = "O"

env.start()
agent = DDQN()
agent.load_state_dict(torch.load(model_path))

print(f"Model: {model_name} {k}k")

sleep = 0

turn = 0
done = False

playerScore = 0
aiScore = 0
p0Score = 0
p1Score = 0

player = None

while True:
    p_inp = input("player 1 or 2 ")
    if not (p_inp == "1" or p_inp == "2"):
        print("Incorrect input, try again.")
        continue
    break
p_inp = int(p_inp)

def convert_to_tensor(state):#oyun durumunu yapay zekaya vermek için hazırlıyor
    toTensor =[]
    for row in state:
        for square in row:
            if square == "S":
                toTensor.append(1)
            elif square == "O":
                toTensor.append(-1)
            else:
                toTensor.append(0)
    return torch.tensor(toTensor, dtype=torch.float)

def getInput():
    mask = env.getMask()
    while True:
        try:
            square_input = int(input("square  "))
        except:
            print("Incorrect input, try again.")
            continue
        if not (0 <= square_input <=35):
            print("Incorrect input, try again.")
            continue
        if mask[square_input] == 0:
            print("This square is not empty, try again.")
            continue
        piece_input = str(input("S or 1 for S,  O or 0 for O ")).upper()
        if piece_input == "Q":
            print("QUIT")
            exit()
        if not (piece_input == "S" or piece_input == "O" or piece_input == "1" or piece_input == "0"):
            print("Incorrect input, try again.")
            continue
        if piece_input == "1":
            piece_input = "S"
        if piece_input == "0":
            piece_input = "O"
        return square_input, piece_input

def playerMove():
    global playerScore, turn, done, p0Score, p1Score
    square_input, piece_input = getInput()
    _, moveScore_player, _, done, turn= env.move(square_input, piece_input)
    playerScore += moveScore_player
    if p_inp == 1:
        p0Score = playerScore
    elif p_inp == 2:
        p1Score = playerScore

def aiMove():
    global aiScore, turn, done, p0Score, p1Score
    inputs = convert_to_tensor(env.board)
    with torch.no_grad():
        outputs = agent(inputs)
    mask = env.getMask()
    q_values = []
    for q, maskValue in zip(outputs, mask):
        if maskValue == 1:
            q_values.append(q)
        else:
            q_values.append(0)
    
    qmax = max(q_values)
    qmin = min(q_values)
    if abs(qmax) > abs(qmin):
        action = (np.argmax(q_values), "S")
    if abs(qmax) < abs(qmin):
        action = (np.argmin(q_values), "O")
    if abs(qmax) == abs(qmin):
        a = random.choice((qmax,qmin))
        if a == qmax:
            action = (np.argmax(q_values), "S")
        elif a == qmin:
            action = (np.argmin(q_values), "O")

    new_state, moveScore_ai, reward, done, turn = env.move(action[0],action[1])
    aiScore += moveScore_ai
    if p_inp == 1:
        p1Score = aiScore
    elif p_inp == 2:
        p0Score = aiScore


while not done:
    if turn == p_inp-1:
        player = "player"
        visualizer.show(turn, player, p0Score, p1Score, waitTime=wait_time)
        playerMove()
    else:
        player = "ai"
        visualizer.show(turn, player, p0Score, p1Score, waitTime=wait_time)
        aiMove()
        time.sleep(sleep)

visualizer.show("over", player, p0Score, p1Score, waitTime=wait_time)
if playerScore > aiScore:
    print("YOU WON")
if playerScore < aiScore:
    print("YOU LOST")
time.sleep(5)