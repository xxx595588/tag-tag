from player import player
import time
import random
import numpy as np

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
    def find_path(self, end, grid, step=1):  
        counter = 0
        vir_raw_x = self.raw_x
        vir_raw_y = self.raw_y
        vir_end_x = end[0]
        vir_end_y = end[1]
       
        while counter < step:
            vir = self.convert_given_coor(vir_raw_x, vir_raw_y)
            vir_x, vir_y = vir[0], vir[1]
            self.map.update_start((vir_x, vir_y))
            self.map.update_end(end)
            self.map.reset()
            self.map.find_shortest_path()
            next_coor = self.map.retrieve()[-1]

            if vir_x - next_coor[0] > 0:
                vir_raw_x += 1
            elif vir_x - next_coor[0] < 0:
                vir_raw_x -= 1
            elif vir_y - next_coor[1] > 0:
                vir_raw_y += 1
            elif vir_y - next_coor[1] < 0:
                vir_raw_y -= 1

            vir = self.convert_given_coor(vir_raw_x, vir_raw_y)
            vir_x, vir_y = vir[0], vir[1]
            
            max_dis = -np.inf
            best_dir = list()

            if grid[3] == "air":
                self.map.update_start((vir_x, vir_y))
                self.map.update_end((vir_end_x, vir_end_y+1))
                self.map.reset()
                self.map.find_shortest_path()
                dis = len(self.map.retrieve())

                if dis >= max_dis:
                    max_dis = dis
                    best_dir.append("movewest")

            if grid[1] == "air":
                self.map.update_start((vir_x, vir_y))
                self.map.update_end((vir_end_x+1, vir_end_y))
                self.map.reset()
                self.map.find_shortest_path()
                dis = len(self.map.retrieve())
                if dis >= max_dis:
                    max_dis = dis
                    best_dir.append("movenorth")

            if grid[5] == "air":
                self.map.update_start((vir_x, vir_y))
                self.map.update_end((vir_end_x, vir_end_y-1))
                self.map.reset()
                self.map.find_shortest_path()
                dis = len(self.map.retrieve())

                if dis >= max_dis:
                    max_dis = dis
                    best_dir.append("moveeast")

            if grid[7] == "air":
                self.map.update_start((vir_x, vir_y))
                self.map.update_end((vir_end_x-1, vir_end_y))
                self.map.reset()
                self.map.find_shortest_path()
                dis = len(self.map.retrieve())

                if dis >= max_dis:
                    max_dis = dis
                    best_dir.append("movesouth")


            best_pred = random.choice(best_dir)

            if best_pred == "movewest":
                vir_end_y += 1
            elif best_pred == "movenorth":
                vir_end_x += 1
            elif best_pred == "moveeast":
                vir_end_y -= 1
            elif best_pred == "movesouth":
                vir_end_x -= 1

            counter += 1

        self.map.update_start(self.convert_coor())
        self.map.update_end((vir_end_x, vir_end_y))
        self.map.reset()
        self.map.find_shortest_path()
        self.find_direction(self.map.retrieve()[-1])