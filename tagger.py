from player import player
from map import map
import time

"""
The class for tagger which inherited from player class
"""
class tagger(player):
    def __init__(self, MALMO_agent, map_txt, x, y):
        player.__init__(self, MALMO_agent, map_txt, x, y)
    
    """ 
    This function will determine the next action and update tagger's coordinate
    """
    def find_direction(self, next_coor):
        (x, y) = self.convert_coor()

        time.sleep(0.2)
        if x - next_coor[0] > 0:
            self.raw_x += 1
            self.MALMO_agent.sendCommand("movesouth")
        elif x - next_coor[0] < 0:
            self.raw_x -= 1
            self.MALMO_agent.sendCommand("movenorth")
        elif y - next_coor[1] > 0:
            self.raw_y += 1
            self.MALMO_agent.sendCommand("moveeast")
        elif y - next_coor[1] < 0:
            self.raw_y -= 1
            self.MALMO_agent.sendCommand("movewest")
    
    """
    This function will find the shortest path to runner by calling map's member function
    """
    def find_path(self, end):  
        self.map.update_start(self.convert_coor())
        self.map.update_end(end)
        self.map.reset()
        self.map.find_shortest_path()
        self.find_direction(self.map.retrieve()[-1])