import os
import constants
import numpy as np
import copy
import torch
import time
from tqdm import tqdm
from sos import SOSEnv
from sos_agent import Agent
from torch.utils.tensorboard import SummaryWriter
from visualizer import Visualizer


if not constants.IS_TEST:   # If not test, creating a writer to save logs and creating model directory
    writer = SummaryWriter(flush_secs=5, log_dir = f'logs/{constants.MODEL_NAME}_{int(time.time())}')
    os.mkdir(f"models/{constants.MODEL_NAME}")

visualizer = Visualizer()   # Creating visulaizer
env = SOSEnv()  # Creating environment
visualizer.env = env    # Setting visulaizer env
agent = Agent(env, constants.LOAD_MODEL)    # Creating agent

# Variables to log
suma = 0
draw = 0
winP0 = 0
winP1 = 0


for episode in tqdm(range(1, constants.EPISODES + 1), ascii=True, unit='episodes'): # Loop over episodes
                                                                                    # Using tqdm to see progress

    # Starting environment and creating neccesary variabels
    env.start()
    p0MoveHistory = []
    p1MoveHistory = []
    p0Score = 0
    p1Score = 0
    turn = 0
    done = False

    while not done:
        if turn == 0:   # If turn=0, player 0 is moving
            toAppend = [copy.deepcopy(env.board)]   # Creating an array to append move history
            action = agent.makeMove(env.board)  # Getting model's move
            new_state, moveScore_p0, reward, done, turn = env.move(action[0],action[1]) # Making move on environment
            p0Score += moveScore_p0

            # Appending model's move and reward to toAppend
            toAppend.append(action)
            toAppend.append(reward)
            p0MoveHistory.append(toAppend)  # Appending array to p0MoveHistory
            
            if moveScore_p0>0:  # If p0 gets score, decreasing p1's last move's reward
                p1MoveHistory[-1][2]-=reward*constants.REWARD_DECREASE_RATE/2

            if episode % constants.SHOW_EVERY == 0 and constants.IS_VISUALIZER_ON:
                visualizer.show(turn, p0Score, p1Score) # Displaying the game

            if done:    # If game over, updating log variables and breaking loop
                if p0Score > p1Score:
                    suma += 1
                    winP0 += 1
                if p0Score < p1Score:
                    suma += -1
                    winP1 += 1
                if p0Score == p1Score:
                    draw += 1
                break

        elif turn == 1: # If turn=1, player 1 is moving
                        # Doing same for player 1
            toAppend=[copy.deepcopy(new_state)]
            action2 = agent.makeMove(new_state) 
            _, moveScore_p1, reward, done, turn = env.move(action2[0], action2[1])
            p1Score += moveScore_p1
            toAppend.append(action2)
            toAppend.append(reward)
            p1MoveHistory.append(toAppend)
            if moveScore_p1>0:
                p0MoveHistory[-1][2]-=reward*constants.REWARD_DECREASE_RATE/2

            if episode % constants.SHOW_EVERY == 0 and constants.IS_VISUALIZER_ON:
                visualizer.show(turn, p0Score, p1Score)

            if done:
                if p0Score > p1Score:
                    suma += 1
                    winP0 += 1
                if p0Score < p1Score:
                    suma += -1
                    winP1 += 1
                if p0Score == p1Score:
                    draw += 1
                break

    agent.train(p0MoveHistory, p1MoveHistory)   # Training the model at the end of the game

    if not constants.IS_TEST and (not episode % constants.AGGREGATE_STATS_EVERY or episode == 1):
        # Logging and reseting log variables, and saving the model
        writer.add_scalar('sum', suma, episode)
        writer.add_scalar('epsilon', constants.EPSILON, episode)
        writer.add_scalar('draw', draw, episode)
        writer.add_scalar('winP0', winP0, episode)
        writer.add_scalar('winP1', winP1, episode)
        draw = 0
        suma = 0
        winP0 = 0
        winP1 = 0
        torch.save(agent.model.state_dict(), f'models/{constants.MODEL_NAME}/{constants.MODEL_NAME} {episode//1000}k.model')

    if constants.EPSILON > constants.MIN_EPSILON:   # Decreasing the epsilon value
        constants.EPSILON *= constants.EPSILON_DECAY
        constants.EPSILON = max(constants.MIN_EPSILON, constants.EPSILON)