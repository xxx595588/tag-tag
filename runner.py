from player import player
from qLearingAgent import QL_agent
import math

ACTIONS = ["movesouth", "moveeast", "movenorth", "movewest"]

"""
The class for runner which inherited from player class
"""
class runner(player):
    def __init__(self, MALMO_agent, map_txt, x, y):
        player.__init__(self, MALMO_agent, map_txt, x, y)

        # instance a QL object from QL_agent class in order to find the best next action
        self.QL = QL_agent(ACTIONS, len(self.plain_map[0]), len(self.plain_map))

    """
    This function will return the next best action accoring to current state by calling QL_agent's member functions
    """
    def next_action(self, S):
        terminated = self.is_caught(S[1])
        A = self.QL.choose_action(S)
        next_S, R = self.next_direction(A, S[1])
        self.QL.update_qtable(A, S, next_S, R, terminated)
        return R

    """
    This function will determine the next action and update runner's coordinate
    """
    def next_direction(self, A, pos):
        """
        position 4 is runner's current position

                   W (-x)
                   |
                 6 3 0
        S (+z)-- 7 4 1 --N (-z)
                 8 5 2
                   |
                   E (+x)
    
        """
        (x, y) = self.convert_coor()
        size = len(self.plain_map)
    
        ori_dis = math.sqrt((x-pos[0])**2 + (y-pos[1])**2)

        if A == "movenorth":
            if size-x-2 >= 0 and self.plain_map[y][size-x-2] != 1:
                self.MALMO_agent.sendCommand("movenorth")
                self.raw_x -= 1
        elif A == "movesouth":
            if size-x < size and self.plain_map[y][size-x] != 1:
                self.MALMO_agent.sendCommand("movesouth")
                self.raw_x += 1     
        elif A == "movewest":
            if y+1 < size and self.plain_map[y+1][size-x-1] != 1:
                self.MALMO_agent.sendCommand("movewest")
                self.raw_y -= 1   
        elif A == "moveeast":
            if y-1 >= 0 and self.plain_map[y-1][size-x-1] != 1:
                self.MALMO_agent.sendCommand("moveeast")
                self.raw_y += 1
                
        (x, y) = self.convert_coor()
        next_S = ((x, y), pos)
        new_dis = math.sqrt((x-pos[0])**2 + (y-pos[1])**2)

        if new_dis <= 1:
            reward = -200
        elif new_dis == math.sqrt(2):
            reward = -100
        elif new_dis < ori_dis:
            reward = 100*(new_dis - ori_dis)/ori_dis
        elif new_dis == ori_dis:
            reward = -5
        else:
            reward = 10

        return next_S, reward

    """
    This function will determine if the game is terminated
    """
    def is_caught(self, pos):
        (x, y) = self.convert_coor()

        if (x-pos[0])**2+(y-pos[1])**2 <= 1:
            return True
        return False
    
    """
    This function will expor the q table as csv file
    """
    def export_qtable(self):
        self.QL.export_data()   