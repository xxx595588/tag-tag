from itertools import permutations 
import numpy as np
import pandas as pd
import random

"""
This class will be a runner class member variable and will be utilized to help runner make the decision

Arguments
    epsilon: <float>  randomness        (default = 0.05)
    alpha:   <float>  learning rate      (default = 0.3)
    gamma:   <float>  value decay rate   (default = 1)
"""
class QL_agent():
    def __init__(self, actions, width, height, epsilon=0.05, alpha=0.3, gamma=1):
        self.actions = actions
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.states = []

        coor = []
        for i in range(height):
            for j in range(width):
                coor.append((i, j))

        self.states = list(permutations(coor, 2))

        for i in range(height):
            for j in range(width):
                self.states.append(((i, j), (i, j)))

        self.states = pd.MultiIndex.from_tuples(self.states, names=["runner", "tagger"])
        self.qtable = pd.DataFrame(np.zeros((len(self.states), len(self.actions))), columns = self.actions, index = self.states)

    """
    This function will return the best action under current state
    """
    def choose_action(self, S):
        rnd = random.random()

        # take random action
        if rnd < self.epsilon:
            return random.choice(self.actions)
        else:
            # find the best movement
            state_data = self.qtable.loc(axis=0)[[S[0]], [S[1]]].values[0]
            ind = [i for i, k in enumerate(state_data) if k == max(state_data)]

            candidate = []
            
            for i in ind:
                candidate.append(self.actions[i])
            if len(ind) > 1:
                return random.choice(candidate)
            else:
                return candidate[0]
    
    """
    This function will update the q table according to the feedback
    """
    def update_qtable(self, A, S, next_S, R, terminated):
        i = self.actions.index(A)
        q = self.qtable.loc(axis=0)[[S[0]], [S[1]]].values[0][i]

        if not terminated:
            est = R + self.gamma*max(self.qtable.loc(axis=0)[[next_S[0]], [next_S[1]]].values[0])
        else:
            est = R

        self.qtable.loc[(S[0], S[1]), [A]] = q + self.alpha*(est-q)

    def export_data(self):
        self.qtable.to_csv("qtable.csv")
