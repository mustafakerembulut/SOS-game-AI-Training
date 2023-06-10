import torch
from torch import nn
from torch.nn import MSELoss
import numpy as np
import constants
import random

class DDQN(nn.Module):  # Double Q Learning model class
    def __init__(self):
        super().__init__()
        self.createModel()

    def createModel(self):  # Creating layers of model
                            # Due to our game playing on 6x6 tabel, our model takes 36 values as input and give us 36 values as output
        self.layer1 = nn.Linear(36, 144)    # Layer 1 takes 36 input and gives 144 output
        self.layer2 = nn.Linear(144, 288)   # ...
        self.layer3 = nn.Linear(288, 288)
        self.layer4 = nn.Linear(288, 144)
        self.layer5 = nn.Linear(144, 36)

    def forward(self, state):   # Running the model and returning output
        x = self.layer1(state)
        x = torch.relu(x)

        x = self.layer2(x)
        x = torch.relu(x)

        x = self.layer3(x)
        x = torch.relu(x)

        x = self.layer4(x)
        x = torch.relu(x)

        x = self.layer5(x)
        x = torch.tanh(x)
        return x    # Returning model's output

class Agent():  # Creating agent
    def __init__(self, env, load=False):
        self.env = env

        self.model = DDQN()
        self.target_model = DDQN()
        
        if load:    # If new model will be trained over a trained model, loading the trained model
            self.model.load_state_dict(torch.load(constants.MODEL_PATH))

        self.target_model.load_state_dict(self.model.state_dict())
        self.target_model = self.target_model.eval()

        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=constants.LR)  # Using stochastic gradient descent as optimizer
        self.loss_function = MSELoss()  # Using mean square error as loss function

        self.target_update_counter = 0

    def backpropagate(self, state, move, reward):   # Updating Q values
        self.optimizer.zero_grad()
        output = self.model(self.convert_to_tensor(state))
        target = output.clone().detach()
        ex_q = target[move[0]]

        if reward >=0:  # If model's move is good
                        # (if reward 0, not changing Q value)
            if move[1]=="S":    # If move S, increasing the Q value     (max 1)
                target_value = ex_q + (1-ex_q)*(reward*constants.REWARD_INCREASE_RATE)
            elif move[1]=="O":  # If move O, decreasing the Q value     (min -1)
                target_value = ex_q + (-1-ex_q)*(reward*constants.REWARD_INCREASE_RATE)

        else:   # If model's move is bad
            if move[1]=="S":    # If move S, decreasing the Q value     (min 0)
                target_value = ex_q + (ex_q)*(reward*constants.REWARD_DECREASE_RATE)
            elif move[1]=="O":  # If move O, increasing the Q value     (max 0)
                target_value = ex_q + (ex_q)*(reward*constants.REWARD_DECREASE_RATE)
        
        target[move[0]] = target_value  # Changing the move's Q value

        loss = self.loss_function(output, target)   # Calculating loss between first model and q values updated model
        loss.backward()
        self.optimizer.step()   # According to the loss changing weights of the model


    def get_qs(self, state, model): # Getting model's output form current state of game
        inputs = self.convert_to_tensor(state)
        with torch.no_grad():
            outputs = model(inputs)
        return outputs
    
    def convert_to_tensor(self, state): # Converting our game state to tensor form
        toTensor =[]
        for row in state:
            for square in row:
                if square == "S":   # If there is S in square, putting 1
                    toTensor.append(1)
                elif square == "O": # If O, -1
                    toTensor.append(-1)
                else:   # If square is empty, 0
                    toTensor.append(0)
        return torch.tensor(toTensor, dtype=torch.float)
    
    def makeMove(self, state):  # Making move

        if np.random.random() > constants.EPSILON:  # Picking a number between 0-1 randomly, if it is greater than epsilon, model making move
            mask = self.env.getMask()
            q_values = []
            for q, maskValue in zip(self.get_qs(state, self.model), mask):  # Getting model's output and legal moves
                                                                            # Changing illegal move's Q values to 0
                if maskValue == 1:
                    q_values.append(q)
                else:
                    q_values.append(0)

            # Getting maximum and minimum Q values
            qmax = max(q_values)
            qmin = min(q_values)

            if abs(qmax) > abs(qmin):   # If absolutes value of qmax greater than absolute value of qmin, moving S to qmax's square
                action = (np.argmax(q_values), "S")
            elif abs(qmax) < abs(qmin): # If qmin's absolute value is greater, moving O to qmin's square
                action = (np.argmin(q_values), "O")
            elif abs(qmax) == abs(qmin):# If they are equal, picking randomly between qmin and qmin
                a = random.choice((qmax,qmin))
                if a == qmax:
                    action = (np.argmax(q_values), "S")
                elif a == qmin:
                    action = (np.argmin(q_values), "O")

        else:   # Random move
            legalMoves = self.env.getLegalMoves(self.env.board)
            actionList = []
            for move in legalMoves:
                actionList.append(constants.ACTION_LIST.index(move))
            action = (random.choice(actionList), random.choice(("S","O")))

        return action   # Returning move
    
    def train(self, p0MoveHistory, p1MoveHistory):  # Getting move histories and training model for every move
        for _ in range(len(p1MoveHistory)):
            current_state, action, reward = p1MoveHistory.pop()
            self.backpropagate(current_state, action, reward)

        for _ in range(len(p0MoveHistory)):
            current_state, action, reward = p0MoveHistory.pop()
            self.backpropagate(current_state, action, reward)

        self.target_update_counter += 1
        if self.target_update_counter > constants.UPDATE_TARGET_EVERY:  # Updating model, if update counter reaches update_target_every value
            self.target_model.load_state_dict(self.model.state_dict())
            self.target_update_counter = 0