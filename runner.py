from player import player
from qLearingAgent import QL_agent

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
    This function will calculate the distance to the tagger
    """
    def find_distance(self, pos):
        self.map.update_start(self.convert_coor())
        self.map.update_end(pos)
        self.map.reset()
        self.map.find_shortest_path()

        return len(self.map.retrieve())

    """
    This function will return the next best action accoring to current state by calling QL_agent's member functions
    """
    def next_action(self, S, grid):
        A = self.QL.choose_action(S)
        next_S, R, terminated= self.next_direction(A, S[1], grid)
        self.QL.update_qtable(A, S, next_S, R, terminated)
        return terminated
    
    def is_surrounded(self, grid):
        if grid[3] == "air" and grid[1] == "bedrock" and grid[7] == "bedrock" and grid[5] == "bedrock":
            return True
        if grid[3] == "bedrock" and grid[1] == "air" and grid[7] == "bedrock" and grid[5] == "bedrock":
            return True
        if grid[3] == "bedrock" and grid[1] == "bedrock" and grid[7] == "air" and grid[5] == "bedrock":
            return True
        if grid[3] == "bedrock" and grid[1] == "bedrock" and grid[7] == "bedrock" and grid[5] == "air":
            return True
        
        return False

    """
    This function will determine the next action and update runner's coordinate
    """
    def next_direction(self, A, pos, grid):
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
        
        surrounded = self.is_surrounded(grid)
        ori_dis = self.find_distance(pos)

        if A == "movenorth" and grid[1] == "air":
            self.MALMO_agent.sendCommand("movenorth")
            self.raw_x -= 1
        elif A == "movesouth" and grid[7] == "air":
            self.MALMO_agent.sendCommand("movesouth")
            self.raw_x += 1
        elif A == "movewest" and grid[3] == "air":
            self.MALMO_agent.sendCommand("movewest")
            self.raw_y -= 1
        elif A == "moveeast" and grid[5] == "air":
            self.MALMO_agent.sendCommand("moveeast")
            self.raw_y += 1                
        
        next_S = (self.convert_coor(), pos)
        new_dis = self.find_distance(pos)

        terminated = self.is_caught(pos)
        
        if terminated:
            reward = -5000
        elif surrounded:
            if new_dis < ori_dis and new_dis >= 3: 
                reward = 50*ori_dis
            else:
                reward = 1000*(new_dis - ori_dis)/ori_dis
        elif new_dis < ori_dis:
            reward = 1000*(new_dis - ori_dis)/ori_dis
        elif new_dis == ori_dis:
            reward = -2000
        else:
            reward = 50*(new_dis - ori_dis)*new_dis

        return next_S, reward, terminated

    """
    This function will determine if the game is terminated
    """
    def is_caught(self, pos):
        (x, y) = self.convert_coor()
        
        if (x-pos[0])**2+(y-pos[1])**2 <= 1:
            return True
        return False
    
    """
    This function will export the q table as csv file
    """
    def export_qtable(self):
        self.QL.export_data()   