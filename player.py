import MalmoPython
import numpy as np
from map import map

"""
The base class for both runner and tagger
"""
class player():
    def __init__(self, MALMO_agent, map_txt, x, y):
        self.MALMO_agent = MALMO_agent
        self.plain_map = map_txt
        self.map = map(map_txt)
        self.raw_x = x
        self.raw_y = y

    """
    This function will convert the coordinate in Minecraft into our map coordinate
    """
    def convert_coor(self):
        return (int(len(self.plain_map)/2-self.raw_x+1), abs(int(self.raw_y)))
    
    """ 
    This function will return the MALMO agent
    """
    def getAgent(self):
        return self.MALMO_agent
    
    """ 
    This function will teleport the agent to specific location
    """
    def teleport(self, x, z):
        self.raw_x = z
        self.raw_y = x
        s = "tp " + str(x) + " 2 " + str(z)
        self.MALMO_agent.sendCommand(s)