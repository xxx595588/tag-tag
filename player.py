import MalmoPython
import numpy as np
import json
import time
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
    
    def convert_given_coor(self, raw_x, raw_y):
        return (int(len(self.plain_map)/2-raw_x+1), abs(int(raw_y)))
    
    """ 
    This function will return the MALMO agent
    """
    def getAgent(self):
        return self.MALMO_agent
    
    """
    This function will return surrounded block as list
    """
    def getEnvir(self):
        time.sleep(0.2)
        world_state = self.MALMO_agent.getWorldState()
        msg = world_state.observations[0].text
        observations = json.loads(msg)
        
        return observations.get(f"floor3x3", 0)
    
    """ 
    This function will teleport the agent to specific location
    """
    def teleport(self, x, z):
        self.raw_x = z
        self.raw_y = x
        s = "tp " + str(x) + " 2 " + str(z)
        self.MALMO_agent.sendCommand(s)