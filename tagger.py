from player import player
from map import map

"""
The class for tagger which inherited from player class
"""
class tagger(player):
    def __init__(self, MALMO_agent, map_txt, x, y):
        player.__init__(self, MALMO_agent, map_txt, x, y)

        # instance a map object from map class in order to find the shortest path to runner
        self.map = map(self.plain_map)
    
    """ 
    This function will determine the next action and update tagger's coordinate
    """
    def find_direction(self, next_coor):
        (x, y) = self.convert_coor()

        if x - next_coor[0] > 0:
            self.raw_x += 1
            return "movesouth"
        elif x - next_coor[0] < 0:
            self.raw_x -= 1
            return "movenorth"
        elif y - next_coor[1] > 0:
            self.raw_y += 1
            return "moveeast"
        elif y - next_coor[1] < 0:
            self.raw_y -= 1
            return "movewest"
    
    """
    This function will find the shortest path to runner by calling map's member function
    """
    def find_path(self, end):  
        self.map.update_start(self.convert_coor())
        self.map.update_end(end)
        self.map.reset()
        self.map.find_shortest_path()
        next_action = self.find_direction(self.map.retrieve()[-1])
        self.MALMO_agent.sendCommand(next_action)